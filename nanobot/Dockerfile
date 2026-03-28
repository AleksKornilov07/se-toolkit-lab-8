# Multi-stage build for nanobot gateway
FROM astral/uv:python3.14-bookworm-slim AS builder

WORKDIR /app

# Copy workspace root files
COPY --from=workspace pyproject.toml uv.lock ./

# Copy mcp folder (includes mcp_lms and mcp_observability)
COPY --from=workspace mcp ./mcp/

# Copy nanobot folder
COPY --from=workspace nanobot ./nanobot/

# Copy nanobot-websocket-channel folder
COPY --from=workspace nanobot-websocket-channel ./nanobot-websocket-channel/

# Sync dependencies from nanobot directory
WORKDIR /app/nanobot
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen

# Production stage
FROM python:3.14.2-slim-bookworm

# Install gosu for running as non-root
RUN apt-get update && apt-get install -y --no-install-recommends gosu && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN groupadd --system --gid 999 nonroot \
    && useradd --system --gid 999 --uid 999 --create-home nonroot

# Copy application from builder
COPY --from=builder --chown=nonroot:nonroot /app /app

# Create qwen directory for credentials
RUN mkdir -p /home/nonroot/.qwen && chown nonroot:nonroot /home/nonroot/.qwen

WORKDIR /app/nanobot

USER nonroot

ENTRYPOINT ["python", "/app/nanobot/entrypoint.py"]
