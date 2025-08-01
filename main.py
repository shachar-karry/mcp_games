#!/usr/bin/env python3

from fastmcp import FastMCP
from laser_gun_interface import LaserGunInterface
from tool_registry import create_tool_registry
from mangum import Mangum

# Create the MCP server
server = FastMCP("acme-laser-guns-server")

# Initialize the laser gun interface
laser_interface = LaserGunInterface()

# Create and register all tools using the registry
registry = create_tool_registry(server, laser_interface)
registry.register_all_tools()

# Convert FastMCP server to Starlette app (always available)
app = server.http_app()

# Create Mangum handler for AWS Lambda
handler = Mangum(app)

if __name__ == "__main__":
    # Run the server with HTTP transport for web deployment
    import os
    port = int(os.environ.get("PORT", 8000))
    server.run(transport="http", host="0.0.0.0", port=port)
    