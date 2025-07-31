#!/usr/bin/env python3

from laser_gun_interface import LaserGunInterface

def test_server_functions():
    """Simple test of all server functions using the interface directly."""
    
    print("🔫 Testing Acme Laser Guns Server Functions")
    print("=" * 50)
    
    # Initialize the interface
    interface = LaserGunInterface()
    
    # Test 1: Get all laser guns
    print("\n1️⃣ Testing: Get all laser guns")
    result = interface.get_all_laser_guns()
    print(f"Found {len(result)} laser guns:")
    for model, specs in result.items():
        print(f"  - {specs['name']} ({specs['model']}) - {specs['price']}")
    
    # Test 2: Get specific model
    print("\n2️⃣ Testing: Get specific model")
    result = interface.get_laser_gun_by_model("photon_blaster_2000")
    if result:
        print(f"Found: {result['name']} - Power: {result['power_output']}, Range: {result['range']}")
    else:
        print("Model not found")
    
    # Test 3: Get by category
    print("\n3️⃣ Testing: Get by category")
    result = interface.get_laser_guns_by_category("Handheld")
    print(f"Found {len(result)} handheld weapons:")
    for model, specs in result.items():
        print(f"  - {specs['name']}")
    
    # Test 4: Get by price range
    print("\n4️⃣ Testing: Get by price range ($500-$2000)")
    result = interface.get_laser_guns_by_price_range(500, 2000)
    print(f"Found {len(result)} weapons in price range:")
    for model, specs in result.items():
        print(f"  - {specs['name']} - {specs['price']}")
    
    # Test 5: Get random gun
    print("\n5️⃣ Testing: Get random laser gun")
    result = interface.get_random_laser_gun()
    print(f"Random gun: {result['name']} ({result['model']}) - {result['price']}")
    
    # Test 6: Compare guns
    print("\n6️⃣ Testing: Compare two guns")
    result = interface.compare_laser_guns("photon_blaster_2000", "quantum_destroyer_xl")
    if "error" not in result:
        print("Comparison:")
        print(f"  Power: {result['comparison']['power_difference']}")
        print(f"  Range: {result['comparison']['range_difference']}")
        print(f"  Price: {result['comparison']['price_difference']}")
    else:
        print(f"Error: {result['error']}")
    
    # Test 7: Get company info
    print("\n7️⃣ Testing: Get company info")
    result = interface.get_acme_corp_info()
    print(f"Company: {result['company']}")
    print(f"Division: {result['division']}")
    print(f"Total models: {result['total_models']}")
    print(f"Price range: {result['price_range']['lowest']} - {result['price_range']['highest']}")
    
    print("\n✅ All tests completed!")

if __name__ == "__main__":
    test_server_functions() 