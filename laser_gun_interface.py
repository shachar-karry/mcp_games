#!/usr/bin/env python3

import json
import random
from typing import Dict, List, Optional

class LaserGunInterface:
    """Interface for accessing and querying laser gun data from Acme Corp."""
    
    def __init__(self, data_file: str = 'laser_guns.json'):
        """Initialize the interface with laser gun data."""
        self.data_file = data_file
        self.laser_guns = self._load_laser_guns()
    
    def _load_laser_guns(self) -> Dict:
        """Load laser gun data from JSON file."""
        try:
            with open(self.data_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Warning: {self.data_file} not found. Using empty database.")
            return {}
    
    def get_all_laser_guns(self) -> Dict[str, Dict]:
        """Get specifications for all available laser guns from Acme Corp."""
        return self.laser_guns
    
    def get_laser_gun_by_model(self, model: str) -> Optional[Dict]:
        """Get specifications for a specific laser gun by model name."""
        return self.laser_guns.get(model, None)
    
    def get_laser_guns_by_category(self, category: str) -> Dict[str, Dict]:
        """Get all laser guns in a specific category."""
        return {model: specs for model, specs in self.laser_guns.items() 
                if specs["category"].lower() == category.lower()}
    
    def get_laser_guns_by_price_range(self, min_price: float, max_price: float) -> Dict[str, Dict]:
        """Get laser guns within a specific price range (in USD)."""
        result = {}
        for model, specs in self.laser_guns.items():
            # Extract price as float (remove $ and ,)
            price_str = specs["price"].replace("$", "").replace(",", "")
            price = float(price_str)
            if min_price <= price <= max_price:
                result[model] = specs
        return result
    
    def get_random_laser_gun(self) -> Dict:
        """Get specifications for a randomly selected laser gun."""
        if not self.laser_guns:
            return {"error": "No laser guns available"}
        model = random.choice(list(self.laser_guns.keys()))
        return {"model": model, **self.laser_guns[model]}
    
    def compare_laser_guns(self, model1: str, model2: str) -> Dict:
        """Compare specifications between two laser gun models."""
        gun1 = self.laser_guns.get(model1)
        gun2 = self.laser_guns.get(model2)
        
        if not gun1 or not gun2:
            return {"error": "One or both models not found"}
        
        comparison = {
            "model1": {model1: gun1},
            "model2": {model2: gun2},
            "comparison": {
                "power_difference": f"{gun1['power_output']} vs {gun2['power_output']}",
                "range_difference": f"{gun1['range']} vs {gun2['range']}",
                "price_difference": f"{gun1['price']} vs {gun2['price']}",
                "weight_difference": f"{gun1['weight']} vs {gun2['weight']}"
            }
        }
        
        return comparison
    
    def get_acme_corp_info(self) -> Dict:
        """Get information about Acme Corp and their laser gun division."""
        if not self.laser_guns:
            return {"error": "No laser guns available"}
        
        # Convert prices to numbers for proper comparison
        prices = []
        for specs in self.laser_guns.values():
            price_str = specs["price"].replace("$", "").replace(",", "")
            prices.append(float(price_str))
            
        return {
            "company": "Acme Corporation",
            "division": "Advanced Weapons Systems",
            "founded": "1985",
            "headquarters": "Futuristic City, Mars Colony",
            "specialization": "High-energy directed weapons",
            "slogan": "When you absolutely, positively need to vaporize something",
            "total_models": len(self.laser_guns),
            "categories_available": list(set(specs["category"] for specs in self.laser_guns.values())),
            "price_range": {
                "lowest": f"${int(min(prices)):,}" if min(prices) >= 1000 else f"${int(min(prices))}",
                "highest": f"${int(max(prices)):,}"
            }
        } 