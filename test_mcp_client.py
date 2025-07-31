#!/usr/bin/env python3

import asyncio
import json
import sys
import requests
from mcp import ClientSession, StdioServerParameters
from mcp import stdio_client

async def test_mcp_server(use_deployed=False):
    """Test the MCP server using the MCP protocol."""
    
    if use_deployed:
        print("🔗 Testing Deployed Acme Laser Guns MCP Server")
        print("🌐 URL: https://mcp-games.onrender.com")
        print("❌ HTTP MCP client not available - using direct HTTP requests instead")
        print("=" * 50)
        
        # For deployed server, we'll use HTTP requests
        
        base_url = "https://mcp-games.onrender.com"
        
        print("1️⃣ Testing: Get all laser guns")
        try:
            response = requests.post(f"{base_url}/mcp/", json={
                "jsonrpc": "2.0",
                "id": 1,
                "method": "tools/call",
                "params": {"name": "get_all_laser_guns", "arguments": {}}
            }, timeout=10)
            
            if response.status_code == 200:
                data = response.json()["result"]
                print(f"✅ Found {len(data)} laser guns:")
                for model, specs in data.items():
                    print(f"  - {specs['name']} ({specs['model']}) - {specs['price']}")
            else:
                print(f"❌ Error: {response.status_code}")
        except Exception as e:
            print(f"❌ Request failed: {e}")
            
        print("\n2️⃣ Testing: Get company info")
        try:
            response = requests.post(f"{base_url}/mcp/", json={
                "jsonrpc": "2.0",
                "id": 2,
                "method": "tools/call",
                "params": {"name": "get_acme_corp_info", "arguments": {}}
            }, timeout=10)
            
            if response.status_code == 200:
                data = response.json()["result"]
                print(f"✅ Company: {data['company']}")
                print(f"   Division: {data['division']}")
                print(f"   Total models: {data['total_models']}")
            else:
                print(f"❌ Error: {response.status_code}")
        except Exception as e:
            print(f"❌ Request failed: {e}")
            
        print("\n✅ Deployed server test completed!")
        return
    
    print("🔗 Connecting to Local Acme Laser Guns MCP Server")
    print("=" * 50)
    
    # Connect to the server using stdio transport
    server_params = StdioServerParameters(
        command="python",
        args=["main_local.py"]
    )
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize the session
            await session.initialize()
            
            # List available tools
            tools = await session.list_tools()
            print(f"\n📋 Available tools: {len(tools.tools)}")
            for tool in tools.tools:
                print(f"  - {tool.name}: {tool.description}")
            
            # Test 1: Get all laser guns
            print("\n1️⃣ Testing: Get all laser guns")
            result = await session.call_tool("get_all_laser_guns", {})
            data = json.loads(result.content[0].text)
            print(f"Found {len(data)} laser guns:")
            for model, specs in data.items():
                print(f"  - {specs['name']} ({specs['model']}) - {specs['price']}")
            
            # Test 2: Get specific model
            print("\n2️⃣ Testing: Get specific model")
            result = await session.call_tool("get_laser_gun_by_model", {"model": "photon_blaster_2000"})
            data = json.loads(result.content[0].text)
            if data:
                print(f"Found: {data['name']} - Power: {data['power_output']}, Range: {data['range']}")
            else:
                print("Model not found")
            
            # Test 3: Get by category
            print("\n3️⃣ Testing: Get by category")
            result = await session.call_tool("get_laser_guns_by_category", {"category": "Handheld"})
            data = json.loads(result.content[0].text)
            print(f"Found {len(data)} handheld weapons:")
            for model, specs in data.items():
                print(f"  - {specs['name']}")
            
            # Test 4: Get by price range
            print("\n4️⃣ Testing: Get by price range ($500-$2000)")
            result = await session.call_tool("get_laser_guns_by_price_range", {"min_price": 500, "max_price": 2000})
            data = json.loads(result.content[0].text)
            print(f"Found {len(data)} weapons in price range:")
            for model, specs in data.items():
                print(f"  - {specs['name']} - {specs['price']}")
            
            # Test 5: Get random gun
            print("\n5️⃣ Testing: Get random laser gun")
            result = await session.call_tool("get_random_laser_gun", {})
            data = json.loads(result.content[0].text)
            print(f"Random gun: {data['name']} ({data['model']}) - {data['price']}")
            
            # Test 6: Compare guns
            print("\n6️⃣ Testing: Compare two guns")
            result = await session.call_tool("compare_laser_guns", {
                "model1": "photon_blaster_2000", 
                "model2": "quantum_destroyer_xl"
            })
            data = json.loads(result.content[0].text)
            if "error" not in data:
                print("Comparison:")
                print(f"  Power: {data['comparison']['power_difference']}")
                print(f"  Range: {data['comparison']['range_difference']}")
                print(f"  Price: {data['comparison']['price_difference']}")
            else:
                print(f"Error: {data['error']}")
            
            # Test 7: Get company info
            print("\n7️⃣ Testing: Get company info")
            result = await session.call_tool("get_acme_corp_info", {})
            data = json.loads(result.content[0].text)
            print(f"Company: {data['company']}")
            print(f"Division: {data['division']}")
            print(f"Total models: {data['total_models']}")
            print(f"Price range: {data['price_range']['lowest']} - {data['price_range']['highest']}")
            
            print("\n✅ All MCP server tests completed!")

if __name__ == "__main__":
    # Check command line arguments
    use_deployed = len(sys.argv) > 1 and sys.argv[1] == "--deployed"
    
    if use_deployed:
        asyncio.run(test_mcp_server(use_deployed=True))
    else:
        asyncio.run(test_mcp_server(use_deployed=False)) 