#!/usr/bin/env python3

from fastmcp import FastMCP
from laser_gun_interface import LaserGunInterface

# Create the MCP server
server = FastMCP("acme-laser-guns-server")

# Initialize the laser gun interface
laser_interface = LaserGunInterface()

# Register MCP tools
@server.tool()
def get_all_laser_guns():
    """Get specifications for all available laser guns from Acme Corp."""
    return laser_interface.get_all_laser_guns()

@server.tool()
def get_laser_gun_by_model(model: str):
    """Get specifications for a specific laser gun by model name."""
    return laser_interface.get_laser_gun_by_model(model)

@server.tool()
def get_laser_guns_by_category(category: str):
    """Get all laser guns in a specific category."""
    return laser_interface.get_laser_guns_by_category(category)

@server.tool()
def get_laser_guns_by_price_range(min_price: float, max_price: float):
    """Get laser guns within a specific price range (in USD)."""
    return laser_interface.get_laser_guns_by_price_range(min_price, max_price)

@server.tool()
def get_random_laser_gun():
    """Get specifications for a randomly selected laser gun."""
    return laser_interface.get_random_laser_gun()

@server.tool()
def compare_laser_guns(model1: str, model2: str):
    """Compare specifications between two laser gun models."""
    return laser_interface.compare_laser_guns(model1, model2)

@server.tool()
def get_acme_corp_info():
    """Get information about Acme Corp and their laser gun division."""
    return laser_interface.get_acme_corp_info()

if __name__ == "__main__":
    # Run the server with HTTP transport for web deployment
    import os
    port = int(os.environ.get("PORT", 8000))
    server.run(transport="http", port=port) 