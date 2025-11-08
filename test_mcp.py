#!/usr/bin/env python3
"""
Test Resume MCP Server - Verify all endpoints work
"""
import requests
import json
import sys

BASE_URL = "http://localhost:8000"
NGROK_URL = None

def get_ngrok_url():
    """Get current ngrok public URL"""
    try:
        response = requests.get("http://127.0.0.1:4040/api/tunnels", timeout=2)
        data = response.json()
        tunnels = data.get("tunnels", [])
        if tunnels:
            return tunnels[0].get("public_url")
    except:
        pass
    return None

def test_endpoint(url, method="GET", data=None):
    """Test an endpoint"""
    try:
        if method == "GET":
            response = requests.get(url, timeout=5)
        else:
            response = requests.post(url, json=data, headers={"Content-Type": "application/json"}, timeout=5)
        
        if response.status_code == 200:
            try:
                return {"status": "OK", "data": response.json()}
            except:
                return {"status": "OK", "data": response.text}
        else:
            return {"status": "ERROR", "code": response.status_code, "data": response.text}
    except Exception as e:
        return {"status": "ERROR", "error": str(e)}

def main():
    global NGROK_URL
    
    print("🧪 Testing Resume MCP Server\n")
    
    # Test 1: Health check
    print("1️⃣ Testing / endpoint...")
    result = test_endpoint(f"{BASE_URL}/")
    print(f"   {result['status']}: {result.get('data', {}).get('status', 'N/A')}\n")
    
    # Test 2: MCP GET (health check)
    print("2️⃣ Testing GET /mcp...")
    result = test_endpoint(f"{BASE_URL}/mcp")
    if result['status'] == "OK":
        data = result.get('data', {})
        print(f"   ✅ Protocol: {data.get('protocol')}")
        print(f"   ✅ Server: {data.get('serverInfo', {}).get('name')}\n")
    else:
        print(f"   ❌ {result}\n")
    
    # Test 3: MCP initialize
    print("3️⃣ Testing POST /mcp (initialize)...")
    result = test_endpoint(f"{BASE_URL}/mcp", "POST", {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "initialize",
        "params": {}
    })
    if result['status'] == "OK":
        data = result.get('data', {})
        print(f"   ✅ Protocol: {data.get('result', {}).get('protocolVersion')}\n")
    else:
        print(f"   ❌ {result}\n")
    
    # Test 4: Tools list
    print("4️⃣ Testing POST /mcp (tools/list)...")
    result = test_endpoint(f"{BASE_URL}/mcp", "POST", {
        "jsonrpc": "2.0",
        "id": 2,
        "method": "tools/list",
        "params": {}
    })
    if result['status'] == "OK":
        data = result.get('data', {})
        tools = data.get('result', {}).get('tools', [])
        print(f"   ✅ Found {len(tools)} tools:")
        for tool in tools:
            print(f"      - {tool.get('name')}")
        print()
    else:
        print(f"   ❌ {result}\n")
    
    # Test 5: Call get_resume_info
    print("5️⃣ Testing POST /mcp (tools/call get_resume_info)...")
    result = test_endpoint(f"{BASE_URL}/mcp", "POST", {
        "jsonrpc": "2.0",
        "id": 3,
        "method": "tools/call",
        "params": {
            "name": "get_resume_info",
            "arguments": {}
        }
    })
    if result['status'] == "OK":
        data = result.get('data', {})
        if 'result' in data:
            content = data['result'].get('content', [])
            if content:
                resume_text = content[0].get('text', '')
                resume = json.loads(resume_text)
                print(f"   ✅ Resume loaded: {resume.get('name')}")
                print(f"   ✅ Skills: {len(resume.get('skills', {}))}")
                print(f"   ✅ Projects: {len(resume.get('projects', []))}\n")
        else:
            print(f"   ❌ Error in response: {data.get('error')}\n")
    else:
        print(f"   ❌ {result}\n")
    
    # Test 6: Check ngrok
    print("6️⃣ Checking ngrok tunnel...")
    NGROK_URL = get_ngrok_url()
    if NGROK_URL:
        print(f"   ✅ ngrok URL: {NGROK_URL}")
        
        # Test public endpoint
        print(f"\n7️⃣ Testing public endpoint {NGROK_URL}/mcp...")
        result = test_endpoint(f"{NGROK_URL}/mcp", "POST", {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/call",
            "params": {
                "name": "get_resume_info",
                "arguments": {}
            }
        })
        if result['status'] == "OK":
            print(f"   ✅ Public endpoint working!\n")
        else:
            print(f"   ❌ Public endpoint error: {result}\n")
    else:
        print(f"   ❌ ngrok not running or not accessible\n")
    
    # Summary
    print("=" * 50)
    print("📋 SUMMARY")
    print("=" * 50)
    print(f"✅ Local server: {BASE_URL}")
    if NGROK_URL:
        print(f"✅ Public URL: {NGROK_URL}/mcp")
        print(f"\n💡 Use this URL in ChatGPT: {NGROK_URL}/mcp")
    else:
        print(f"❌ ngrok not running - start with: ngrok http 8000")
    print()

if __name__ == "__main__":
    main()

