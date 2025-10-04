from fastmcp import FastMCP
import json
import os
import asyncio

# Read config from ~/.canopy/mcp_config.json
config_path = os.path.expanduser("~/.canopy/mcp_config.json")
with open(config_path, "r") as f:
    mcp_config = json.load(f)

print("Config loaded:", mcp_config)


# Create a proxy to the configured server (auto-creates ProxyClient)
proxy = FastMCP.as_proxy(mcp_config, name="Config-Based Proxy")

# Run the proxy with stdio transport for local access
if __name__ == "__main__":
    print("\n=== Starting proxy server ===")
    print("Note: The proxy will start and wait for MCP client connections via stdio")
    print("Press Ctrl+C to stop")
    proxy.run()