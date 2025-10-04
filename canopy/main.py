from fastmcp import FastMCP
from fastmcp.server.middleware import Middleware, MiddlewareContext
import json
import os
import tomllib
import sys
import mcp.types as mt

from policy import CanopyPolicy

class PolicyMiddleware(Middleware):
    def __init__(self, policy: CanopyPolicy):
        super().__init__()
        # Initialize any policy-related state here
        self.policy = policy

    async def on_message(self, context: MiddlewareContext, call_next):
        """Called for all MCP messages."""
        message = context.message

        if isinstance(message, mt.CallToolRequestParams):
            tool_name = message.name

            # Check if allowed
            if not self.policy.is_allowed(tool_name):
                raise Exception(f"Tool call to {tool_name} is not allowed by policy")

            print(f"Processing {context.method} from {context.source} - {tool_name}", file=sys.stderr)
        
        result = await call_next(context)
        
        print(f"Completed {context.method}",file=sys.stderr)
        return result


def load_policy(path: str) -> dict:
    with open(path, "rb") as f:
        return tomllib.load(f)

# Read config from ~/.canopy/mcp_config.json
config_path = os.path.expanduser("~/.canopy/mcp_config.json")
with open(config_path, "r") as f:
    mcp_config = json.load(f)

# Read policy from command line argument if provided
policy_path = sys.argv[1]
flow_policy = load_policy(policy_path)

# Create a proxy to the configured server (auto-creates ProxyClient)
proxy = FastMCP.as_proxy(mcp_config, name="Config-Based Proxy")
proxy.add_middleware(PolicyMiddleware(policy=CanopyPolicy(flow_policy)))

# Run the proxy with stdio transport for local access
if __name__ == "__main__":
    print("\n=== Starting proxy server ===")
    print("Note: The proxy will start and wait for MCP client connections via stdio")
    print("Press Ctrl+C to stop")
    proxy.run()