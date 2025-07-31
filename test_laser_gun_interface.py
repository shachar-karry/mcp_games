#!/usr/bin/env python3

import pytest
import json
import tempfile
import os
from laser_gun_interface import LaserGunInterface

class TestLaserGunInterface:
    """Test suite for LaserGunInterface class."""
    
    @pytest.fixture
    def sample_laser_guns_data(self):
        """Sample laser guns data for testing."""
        return {
            "photon_blaster_2000": {
                "name": "Photon Blaster 2000",
                "model": "PB-2000",
                "manufacturer": "Acme Corp",
                "category": "Handheld",
                "power_output": "2.5 MW",
                "range": "500 meters",
                "ammo_capacity": "50 shots",
                "recharge_time": "3 seconds",
                "weight": "2.3 kg",
                "price": "$1,299",
                "features": ["Auto-targeting", "Variable power settings", "Heat-resistant grip"],
                "color": "Metallic blue",
                "warranty": "2 years"
            },
            "quantum_destroyer_xl": {
                "name": "Quantum Destroyer XL",
                "model": "QD-XL",
                "manufacturer": "Acme Corp",
                "category": "Heavy Weapon",
                "power_output": "15 MW",
                "range": "2.5 km",
                "ammo_capacity": "10 shots",
                "recharge_time": "15 seconds",
                "weight": "45 kg",
                "price": "$8,999",
                "features": ["Multi-target lock", "Shield penetration", "Tactical scope", "Bipod mount"],
                "color": "Stealth black",
                "warranty": "5 years"
            },
            "stun_ray_mini": {
                "name": "Stun Ray Mini",
                "model": "SR-Mini",
                "manufacturer": "Acme Corp",
                "category": "Non-lethal",
                "power_output": "0.1 MW",
                "range": "100 meters",
                "ammo_capacity": "200 shots",
                "recharge_time": "1 second",
                "weight": "0.8 kg",
                "price": "$299",
                "features": ["Stun mode", "Pain mode", "Compact design", "Belt clip"],
                "color": "Tactical green",
                "warranty": "1 year"
            }
        }
    
    @pytest.fixture
    def temp_json_file(self, sample_laser_guns_data):
        """Create a temporary JSON file with sample data."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(sample_laser_guns_data, f)
            temp_file = f.name
        
        yield temp_file
        
        # Cleanup
        os.unlink(temp_file)
    
    @pytest.fixture
    def interface(self, temp_json_file):
        """Create LaserGunInterface instance with test data."""
        return LaserGunInterface(temp_json_file)
    
    def test_load_laser_guns_success(self, interface, sample_laser_guns_data):
        """Test successful loading of laser guns data."""
        assert interface.laser_guns == sample_laser_guns_data
        assert len(interface.laser_guns) == 3
    
    def test_load_laser_guns_file_not_found(self, capsys):
        """Test handling of missing JSON file."""
        interface = LaserGunInterface("nonexistent_file.json")
        captured = capsys.readouterr()
        
        assert "Warning: nonexistent_file.json not found" in captured.out
        assert interface.laser_guns == {}
    
    def test_get_all_laser_guns(self, interface, sample_laser_guns_data):
        """Test getting all laser guns."""
        result = interface.get_all_laser_guns()
        assert result == sample_laser_guns_data
        assert len(result) == 3
    
    def test_get_laser_gun_by_model_success(self, interface):
        """Test getting a specific laser gun by model."""
        result = interface.get_laser_gun_by_model("photon_blaster_2000")
        assert result is not None
        assert result["name"] == "Photon Blaster 2000"
        assert result["model"] == "PB-2000"
        assert result["category"] == "Handheld"
    
    def test_get_laser_gun_by_model_not_found(self, interface):
        """Test getting a non-existent laser gun model."""
        result = interface.get_laser_gun_by_model("nonexistent_model")
        assert result is None
    
    def test_get_laser_guns_by_category_success(self, interface):
        """Test getting laser guns by category."""
        result = interface.get_laser_guns_by_category("Handheld")
        assert len(result) == 1
        assert "photon_blaster_2000" in result
        
        result = interface.get_laser_guns_by_category("Heavy Weapon")
        assert len(result) == 1
        assert "quantum_destroyer_xl" in result
    
    def test_get_laser_guns_by_category_case_insensitive(self, interface):
        """Test category filtering is case insensitive."""
        result = interface.get_laser_guns_by_category("handheld")
        assert len(result) == 1
        assert "photon_blaster_2000" in result
        
        result = interface.get_laser_guns_by_category("HANDHELD")
        assert len(result) == 1
        assert "photon_blaster_2000" in result
    
    def test_get_laser_guns_by_category_empty(self, interface):
        """Test getting laser guns by non-existent category."""
        result = interface.get_laser_guns_by_category("Artillery")
        assert result == {}
    
    def test_get_laser_guns_by_price_range_success(self, interface):
        """Test getting laser guns by price range."""
        result = interface.get_laser_guns_by_price_range(1000, 2000)
        assert len(result) == 1
        assert "photon_blaster_2000" in result
        
        result = interface.get_laser_guns_by_price_range(0, 500)
        assert len(result) == 1
        assert "stun_ray_mini" in result
    
    def test_get_laser_guns_by_price_range_multiple(self, interface):
        """Test getting multiple laser guns in price range."""
        result = interface.get_laser_guns_by_price_range(0, 10000)
        assert len(result) == 3  # All guns should be in this range
    
    def test_get_laser_guns_by_price_range_empty(self, interface):
        """Test getting laser guns by price range with no matches."""
        result = interface.get_laser_guns_by_price_range(50000, 100000)
        assert result == {}
    
    def test_get_random_laser_gun_success(self, interface):
        """Test getting a random laser gun."""
        result = interface.get_random_laser_gun()
        assert "model" in result
        # The model should be one of the model field values from the JSON data
        assert result["model"] in ["PB-2000", "QD-XL", "SR-Mini"]
        assert "name" in result
        assert "manufacturer" in result
    
    def test_get_random_laser_gun_empty_database(self):
        """Test getting random laser gun with empty database."""
        interface = LaserGunInterface("nonexistent_file.json")
        result = interface.get_random_laser_gun()
        assert result == {"error": "No laser guns available"}
    
    def test_compare_laser_guns_success(self, interface):
        """Test comparing two laser guns."""
        result = interface.compare_laser_guns("photon_blaster_2000", "quantum_destroyer_xl")
        
        assert "model1" in result
        assert "model2" in result
        assert "comparison" in result
        assert "photon_blaster_2000" in result["model1"]
        assert "quantum_destroyer_xl" in result["model2"]
        assert "power_difference" in result["comparison"]
        assert "2.5 MW vs 15 MW" in result["comparison"]["power_difference"]
    
    def test_compare_laser_guns_one_not_found(self, interface):
        """Test comparing with one non-existent model."""
        result = interface.compare_laser_guns("photon_blaster_2000", "nonexistent_model")
        assert result == {"error": "One or both models not found"}
    
    def test_compare_laser_guns_both_not_found(self, interface):
        """Test comparing with both non-existent models."""
        result = interface.compare_laser_guns("nonexistent_model1", "nonexistent_model2")
        assert result == {"error": "One or both models not found"}
    
    def test_get_acme_corp_info_success(self, interface):
        """Test getting Acme Corp information."""
        result = interface.get_acme_corp_info()
        
        assert result["company"] == "Acme Corporation"
        assert result["division"] == "Advanced Weapons Systems"
        assert result["founded"] == "1985"
        assert result["headquarters"] == "Futuristic City, Mars Colony"
        assert result["total_models"] == 3
        assert "Handheld" in result["categories_available"]
        assert "Heavy Weapon" in result["categories_available"]
        assert "Non-lethal" in result["categories_available"]
        assert result["price_range"]["lowest"] == "$299"
        assert result["price_range"]["highest"] == "$8,999"
    
    def test_get_acme_corp_info_empty_database(self):
        """Test getting Acme Corp info with empty database."""
        interface = LaserGunInterface("nonexistent_file.json")
        result = interface.get_acme_corp_info()
        assert result == {"error": "No laser guns available"}
    
    def test_interface_initialization_with_custom_file(self, temp_json_file):
        """Test interface initialization with custom file path."""
        interface = LaserGunInterface(temp_json_file)
        assert interface.data_file == temp_json_file
        assert len(interface.laser_guns) == 3

if __name__ == "__main__":
    pytest.main([__file__]) 