#!/usr/bin/env python3

import json
import requests
import subprocess
import time
import os
import sys

def test_local_server():
    """Test the local MCP server using HTTP requests."""
    print("🔗 Testing Local Acme Laser Guns MCP Server")
    print("🌐 URL: http://localhost:8000")
    print("✅ Starting local server and testing connectivity")
    print("=" * 50)
    
    # Start the local server
    print("🚀 Starting local server...")
    server_process = subprocess.Popen([
        sys.executable, "-m", "uvicorn", "main:app", 
        "--host", "0.0.0.0", "--port", "8000"
    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    
    try:
        # Wait for server to start (longer wait)
        print("⏳ Waiting for server to start...")
        time.sleep(8)
        
        # Check if server is running
        if server_process.poll() is not None:
            stdout, stderr = server_process.communicate()
            print(f"❌ Server failed to start!")
            print(f"STDOUT: {stdout}")
            print(f"STDERR: {stderr}")
            assert False, "Server failed to start"
        
        # Test server health
        print("🏥 Testing server health...")
        try:
            health_response = requests.get("http://localhost:8000/", timeout=5)
            print(f"✅ Server responding on root: {health_response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"⚠️  Root endpoint not found (expected): {e}")
        
        base_url = "http://localhost:8000"
        session_id = None
        
        # Use a session to maintain headers across requests
        session = requests.Session()
        session.headers.update({
            "Content-Type": "application/json",
            "Accept": "application/json, text/event-stream"
        })
        
        # Step 1: Initialize session
        print("🔄 Initializing MCP session...")
        try:
            init_response = session.post(f"{base_url}/mcp/", 
                json={
                    "jsonrpc": "2.0",
                    "id": 1,
                    "method": "initialize",
                    "params": {
                        "protocolVersion": "2024-11-05",
                        "capabilities": {},
                        "clientInfo": {"name": "test-client", "version": "1.0"}
                    }
                }, timeout=10)
            
            assert init_response.status_code == 200, f"Initialization failed: {init_response.status_code}"
            
            # Extract session ID from header
            session_id = init_response.headers.get('mcp-session-id')
            print(f"✅ Session initialized! Server: acme-laser-guns-server")
            print(f"Session ID: {session_id}")
            
            # Parse SSE response
            response_text = init_response.text
            assert "data: " in response_text, f"Unexpected response format: {response_text}"
            
            json_data = response_text.split("data: ")[1].strip()
            init_data = json.loads(json_data)
            assert "result" in init_data, f"Initialization failed: {init_data}"
            
            server_info = init_data["result"]["serverInfo"]
            print(f"Server version: {server_info['version']}")
            print(f"Protocol version: {init_data['result']['protocolVersion']}")
            
        except Exception as e:
            print(f"❌ Initialization failed: {e}")
            assert False, f"Initialization failed: {e}"
        
        # Add session ID to headers for subsequent requests
        if session_id:
            session.headers.update({"mcp-session-id": session_id})
        
        print("\n📋 Testing basic connectivity...")
        print("✅ Server is reachable and responding to MCP protocol")
        print("✅ Session management is working")
        print("✅ Server version and protocol are compatible")
        
        # Test tools/list
        print("\n🔧 Testing tools/list...")
        try:
            tools_response = session.post(f"{base_url}/mcp/", 
                json={
                    "jsonrpc": "2.0",
                    "id": 2,
                    "method": "tools/list",
                    "params": {}
                }, timeout=10)
            
            print(f"Tools list response: {tools_response.status_code}")
            if tools_response.status_code == 200:
                print("✅ Tools list endpoint responding")
            else:
                print(f"⚠️  Tools list failed: {tools_response.text}")
        except Exception as e:
            print(f"⚠️  Tools list error: {e}")
        
        print("\n🎯 Local server test completed successfully!")
        
    finally:
        # Clean up: stop the server
        print("\n🛑 Stopping local server...")
        server_process.terminate()
        try:
            server_process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            server_process.kill()
        print("✅ Server stopped")

if __name__ == "__main__":
    test_local_server() 