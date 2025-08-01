#!/usr/bin/env python3

from fastmcp import FastMCP
from laser_gun_interface import LaserGunInterface
from tool_registry import create_tool_registry

# Create the MCP server
server = FastMCP("acme-laser-guns-server")

# Initialize the laser gun interface
laser_interface = LaserGunInterface()

# Create and register all tools using the registry
registry = create_tool_registry(server, laser_interface)
registry.register_all_tools()

if __name__ == "__main__":
    # Run the server with stdio transport for local MCP client testing
    server.run() 