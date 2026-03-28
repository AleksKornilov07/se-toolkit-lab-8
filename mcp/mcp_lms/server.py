"""Stdio MCP server exposing LMS backend operations as typed tools."""

from __future__ import annotations

import asyncio
import json
import os
from collections.abc import Awaitable, Callable, Sequence
from typing import Any

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import TextContent, Tool
from pydantic import BaseModel, Field

from mcp_lms.client import LMSClient

_base_url: str = ""

server = Server("lms")

# ---------------------------------------------------------------------------
# Input models
# ---------------------------------------------------------------------------


class _NoArgs(BaseModel):
    """Empty input model for tools that only need server-side configuration."""


class _LabQuery(BaseModel):
    lab: str = Field(description="Lab identifier, e.g. 'lab-04'.")


class _TopLearnersQuery(_LabQuery):
    limit: int = Field(
        default=5, ge=1, description="Max learners to return (default 5)."
    )


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _resolve_api_key() -> str:
    for name in ("NANOBOT_LMS_API_KEY", "LMS_API_KEY"):
        value = os.environ.get(name, "").strip()
        if value:
            return value
    raise RuntimeError(
        "LMS API key not configured. Set NANOBOT_LMS_API_KEY or LMS_API_KEY."
    )


def _client() -> LMSClient:
    if not _base_url:
        raise RuntimeError(
            "LMS backend URL not configured. Pass it as: python -m mcp_lms <base_url>"
        )
    return LMSClient(_base_url, _resolve_api_key())


def _text(data: BaseModel | Sequence[BaseModel]) -> list[TextContent]:
    """Serialize a pydantic model (or list of models) to a JSON text block."""
    if isinstance(data, BaseModel):
        payload = data.model_dump()
    else:
        payload = [item.model_dump() for item in data]
    return [TextContent(type="text", text=json.dumps(payload, ensure_ascii=False))]


# ---------------------------------------------------------------------------
# Tool handlers
# ---------------------------------------------------------------------------


async def _health(_args: _NoArgs) -> list[TextContent]:
    return _text(await _client().health_check())


async def _labs(_args: _NoArgs) -> list[TextContent]:
    items = await _client().get_items()
    return _text([i for i in items if i.type == "lab"])


async def _learners(_args: _NoArgs) -> list[TextContent]:
    return _text(await _client().get_learners())


async def _pass_rates(args: _LabQuery) -> list[TextContent]:
    return _text(await _client().get_pass_rates(args.lab))


async def _timeline(args: _LabQuery) -> list[TextContent]:
    return _text(await _client().get_timeline(args.lab))


async def _groups(args: _LabQuery) -> list[TextContent]:
    return _text(await _client().get_groups(args.lab))


async def _top_learners(args: _TopLearnersQuery) -> list[TextContent]:
    return _text(await _client().get_top_learners(args.lab, limit=args.limit))


async def _completion_rate(args: _LabQuery) -> list[TextContent]:
    return _text(await _client().get_completion_rate(args.lab))


async def _sync_pipeline(_args: _NoArgs) -> list[TextContent]:
    return _text(await _client().sync_pipeline())


# ---------------------------------------------------------------------------
# Registry: tool name -> (input model, handler, Tool definition)
# ---------------------------------------------------------------------------

_Registry = tuple[type[BaseModel], Callable[..., Awaitable[list[TextContent]]], Tool]

_TOOLS: dict[str, _Registry] = {}


def _register(
    name: str,
    description: str,
    model: type[BaseModel],
    handler: Callable[..., Awaitable[list[TextContent]]],
) -> None:
    schema = model.model_json_schema()
    # Pydantic puts definitions under $defs; flatten for MCP's JSON Schema expectation.
    schema.pop("$defs", None)
    schema.pop("title", None)
    _TOOLS[name] = (
        model,
        handler,
        Tool(name=name, description=description, inputSchema=schema),
    )


_register(
    "lms_health",
    "Check if the LMS backend is healthy and report the item count.",
    _NoArgs,
    _health,
)
_register("lms_labs", "List all labs available in the LMS.", _NoArgs, _labs)
_register(
    "lms_learners", "List all learners registered in the LMS.", _NoArgs, _learners
)
_register(
    "lms_pass_rates",
    "Get pass rates (avg score and attempt count per task) for a lab.",
    _LabQuery,
    _pass_rates,
)
_register(
    "lms_timeline",
    "Get submission timeline (date + submission count) for a lab.",
    _LabQuery,
    _timeline,
)
_register(
    "lms_groups",
    "Get group performance (avg score + student count per group) for a lab.",
    _LabQuery,
    _groups,
)
_register(
    "lms_top_learners",
    "Get top learners by average score for a lab.",
    _TopLearnersQuery,
    _top_learners,
)
_register(
    "lms_completion_rate",
    "Get completion rate (passed / total) for a lab.",
    _LabQuery,
    _completion_rate,
)
_register(
    "lms_sync_pipeline",
    "Trigger the LMS sync pipeline. May take a moment.",
    _NoArgs,
    _sync_pipeline,
)


# ---------------------------------------------------------------------------
# MCP handlers
# ---------------------------------------------------------------------------


@server.list_tools()
async def list_tools() -> list[Tool]:
    return [entry[2] for entry in _TOOLS.values()]


@server.call_tool()
async def call_tool(name: str, arguments: dict[str, Any] | None) -> list[TextContent]:
    entry = _TOOLS.get(name)
    if entry is None:
        return [TextContent(type="text", text=f"Unknown tool: {name}")]

    model_cls, handler, _ = entry
    try:
        args = model_cls.model_validate(arguments or {})
        return await handler(args)
    except Exception as exc:
        return [TextContent(type="text", text=f"Error: {type(exc).__name__}: {exc}")]


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------


async def main(base_url: str | None = None) -> None:
    global _base_url
    _base_url = base_url or os.environ.get("NANOBOT_LMS_BACKEND_URL", "")
    async with stdio_server() as (read_stream, write_stream):
        init_options = server.create_initialization_options()
        await server.run(read_stream, write_stream, init_options)


if __name__ == "__main__":
    asyncio.run(main())


# ============================================================================
# Observability Tools (VictoriaLogs & VictoriaTraces)
# ============================================================================

_logs_url = os.environ.get("VICTORIALOGS_URL", "http://victorialogs:9428").rstrip("/")
_traces_url = os.environ.get("VICTORIATRACES_URL", "http://victoriatraces:10428").rstrip("/")

class _LogsSearchQuery(BaseModel):
    query: str = Field(description="LogsQL query, e.g. 'error', 'level:error'")
    limit: int = Field(default=20, ge=1, le=100, description="Max entries to return")

class _TimeRangeQuery(BaseModel):
    service: str = Field(description="Service name, e.g. 'backend'")
    hours: int = Field(default=1, ge=1, le=24, description="Time range in hours")

class _TraceQuery(BaseModel):
    service: str = Field(description="Service name to search traces for")
    limit: int = Field(default=5, ge=1, le=20, description="Max traces to return")

class _TraceById(BaseModel):
    trace_id: str = Field(description="Trace ID to fetch")

async def _logs_search(args: _LogsSearchQuery) -> list[TextContent]:
    """Search VictoriaLogs using LogsQL."""
    import httpx
    url = f"{_logs_url}/select/logsql/query"
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.get(url, params={"query": args.query, "limit": args.limit}, timeout=30.0)
            resp.raise_for_status()
            return _text(resp.json())
    except Exception as e:
        return _text({"error": str(e)})

async def _logs_error_count(args: _TimeRangeQuery) -> list[TextContent]:
    """Count error logs for a service."""
    import httpx
    query = f'_stream:{{service="{args.service}"}} AND level:error'
    url = f"{_logs_url}/select/logsql/query"
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.get(url, params={"query": query, "limit": 100}, timeout=30.0)
            resp.raise_for_status()
            return _text(resp.json())
    except Exception as e:
        return _text({"error": str(e)})

async def _traces_list(args: _TraceQuery) -> list[TextContent]:
    """List recent traces for a service."""
    import httpx
    url = f"{_traces_url}/jaeger/api/traces"
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.get(url, params={"service": args.service, "limit": args.limit}, timeout=30.0)
            resp.raise_for_status()
            return _text(resp.json())
    except Exception as e:
        return _text({"error": str(e)})

async def _traces_get(args: _TraceById) -> list[TextContent]:
    """Fetch a specific trace by ID."""
    import httpx
    url = f"{_traces_url}/jaeger/api/traces/{args.trace_id}"
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.get(url, timeout=30.0)
            resp.raise_for_status()
            return _text(resp.json())
    except Exception as e:
        return _text({"error": str(e)})

# Register observability tools
_register(
    "logs_search",
    "Search VictoriaLogs using LogsQL query. Returns matching log entries.",
    _LogsSearchQuery,
    _logs_search,
)
_register(
    "logs_error_count",
    "Count error logs for a service. Use to check if there are errors.",
    _TimeRangeQuery,
    _logs_error_count,
)
_register(
    "traces_list",
    "List recent traces for a service. Returns trace summaries.",
    _TraceQuery,
    _traces_list,
)
_register(
    "traces_get",
    "Fetch full details of a specific trace by ID.",
    _TraceById,
    _traces_get,
)

if __name__ == "__main__":
    asyncio.run(main())
