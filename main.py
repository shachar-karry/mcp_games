#!/usr/bin/env python3

from fastmcp import FastMCP
from laser_gun_interface import LaserGunInterface
from tool_registry import create_tool_registry
from starlette.responses import JSONResponse
from starlette.routing import Route

# Create the MCP server
server = FastMCP("acme-laser-guns-server")

# Initialize the laser gun interface
laser_interface = LaserGunInterface()

# Create and register all tools using the registry
registry = create_tool_registry(server, laser_interface)
registry.register_all_tools()

# Get the underlying Starlette app and add health check endpoint
app = server.http_app()

async def health_check(request):
    """Health check endpoint for monitoring and load balancers"""
    return JSONResponse(
        status_code=200,
        content={
            "status": "healthy",
            "service": "acme-laser-guns-server",
            "version": "1.0.0"
        }
    )

# Add the health check route to the app
app.routes.append(Route("/health", health_check, methods=["GET"]))

if __name__ == "__main__":
    # Run the server with uvicorn
    import os
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
    