#!/usr/bin/env python3
"""
Tool registry for Acme Laser Guns MCP Server
Simple, readable tool definitions
"""

from typing import Dict, Any, Callable, Optional, Type

class ToolRegistry:
    """Simple registry for MCP tools"""
    
    def __init__(self, server, interface):
        self.server = server
        self.interface = interface
    
    def register_all_tools(self):
        """Register all laser gun tools"""
        
        @self.server.tool()
        def get_all_laser_guns():
            """Get specifications for all available laser guns from Acme Corp."""
            return self.interface.get_all_laser_guns()
        
        @self.server.tool()
        def get_laser_gun_by_model(model: str):
            """Get specifications for a specific laser gun by model name."""
            return self.interface.get_laser_gun_by_model(model)
        
        @self.server.tool()
        def get_laser_guns_by_category(category: str):
            """Get all laser guns in a specific category."""
            return self.interface.get_laser_guns_by_category(category)
        
        @self.server.tool()
        def get_laser_guns_by_price_range(min_price: float, max_price: float):
            """Get laser guns within a specific price range (in USD)."""
            return self.interface.get_laser_guns_by_price_range(min_price, max_price)
        
        @self.server.tool()
        def get_random_laser_gun():
            """Get specifications for a randomly selected laser gun."""
            return self.interface.get_random_laser_gun()
        
        @self.server.tool()
        def compare_laser_guns(model1: str, model2: str):
            """Compare specifications between two laser gun models."""
            return self.interface.compare_laser_guns(model1, model2)
        
        @self.server.tool()
        def get_acme_corp_info():
            """Get information about Acme Corp and their laser gun division."""
            return self.interface.get_acme_corp_info()

def create_tool_registry(server, interface):
    """Create and configure a tool registry for laser guns"""
    registry = ToolRegistry(server, interface)
    return registry 