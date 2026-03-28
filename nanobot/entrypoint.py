#!/usr/bin/env python3
"""Resolve environment variables into nanobot config and launch gateway."""

import json
import os
import sys
from pathlib import Path

def main():
    # Paths
    script_dir = Path(__file__).parent
    config_path = script_dir / "config.json"
    resolved_path = script_dir / "config.resolved.json"
    workspace = script_dir / "workspace"
    
    # Load base config
    with open(config_path) as f:
        config = json.load(f)
    
    # Resolve provider config from env vars
    provider = config.get("providers", {}).get("openai", {})
    provider["apiKey"] = os.environ.get("LLM_API_KEY", provider.get("apiKey", ""))
    provider["apiBase"] = os.environ.get("LLM_API_BASE_URL", provider.get("apiBase", ""))
    config["providers"]["openai"] = provider
    
    # Resolve gateway config
    if "gateway" not in config:
        config["gateway"] = {}
    config["gateway"]["host"] = os.environ.get("NANOBOT_GATEWAY_CONTAINER_ADDRESS", "0.0.0.0")
    config["gateway"]["port"] = int(os.environ.get("NANOBOT_GATEWAY_CONTAINER_PORT", "18790"))
    
    # Resolve webchat channel config
    if "channels" not in config:
        config["channels"] = {}
    config["channels"]["webchat"] = {
        "enabled": True,
        "allow_from": ["*"],
        "port": int(os.environ.get("NANOBOT_WEBCHAT_CONTAINER_PORT", "8765")),
        "access_key": os.environ.get("NANOBOT_ACCESS_KEY", "")
    }
    
    # Resolve MCP server env vars
    if "tools" not in config:
        config["tools"] = {}
    if "mcpServers" not in config["tools"]:
        config["tools"]["mcpServers"] = {}
    
    # LMS MCP server
    config["tools"]["mcpServers"]["lms"] = {
        "command": "/app/.venv/bin/python",
        "args": ["-m", "mcp_lms"],
        "env": {
            "NANOBOT_LMS_BACKEND_URL": os.environ.get("NANOBOT_LMS_BACKEND_URL", "http://backend:8000"),
            "NANOBOT_LMS_API_KEY": os.environ.get("NANOBOT_LMS_API_KEY", "")
        }
    }
    
    # Write resolved config
    with open(resolved_path, "w") as f:
        json.dump(config, f, indent=2)
    
    print(f"Resolved config written to {resolved_path}")
    
    # Launch nanobot gateway from .venv
    nanobot_bin = "/app/.venv/bin/nanobot"
    os.execvp(nanobot_bin, [nanobot_bin, "gateway", "--config", str(resolved_path), "--workspace", str(workspace)])

if __name__ == "__main__":
    main()
