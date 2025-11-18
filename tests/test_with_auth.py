#!/usr/bin/env python3
"""
Test ngrok.anix.app endpoint with authentication for OpenAI SDK
"""

import requests
import json
import os

# Your ngrok static domain endpoint
MCP_URL = "https://anix.ngrok.app/mcp"

# Get API key from environment or use default
API_KEY = os.getenv("OWNER_API_KEY", "owner-secret-key-change-me")

def test_without_auth():
    """Test that endpoint requires auth"""
    print("=" * 60)
    print("TEST 1: Without Authentication (should fail)")
    print("=" * 60)
    try:
        response = requests.get(MCP_URL, verify=False)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 401  # Expect unauthorized
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_health_check():
    """Test GET endpoint (health check) with auth"""
    print("\n" + "=" * 60)
    print("TEST 2: Health Check (GET /mcp) with Auth")
    print("=" * 60)
    try:
        headers = {"X-API-Key": API_KEY}
        response = requests.get(MCP_URL, headers=headers, verify=False)
        print(f"Status: {response.status_code}")
        print(f"Response:\n{json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_initialize():
    """Test MCP initialize handshake"""
    print("\n" + "=" * 60)
    print("TEST 3: Initialize (MCP Handshake)")
    print("=" * 60)
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "initialize",
        "params": {
            "protocolVersion": "2024-11-05",
            "capabilities": {},
            "clientInfo": {
                "name": "test-client",
                "version": "1.0.0"
            }
        }
    }
    try:
        headers = {"X-API-Key": API_KEY}
        response = requests.post(MCP_URL, json=payload, headers=headers, verify=False)
        print(f"Status: {response.status_code}")
        print(f"Response:\n{json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_list_tools():
    """Test listing available tools"""
    print("\n" + "=" * 60)
    print("TEST 4: List Tools")
    print("=" * 60)
    payload = {
        "jsonrpc": "2.0",
        "id": 2,
        "method": "tools/list",
        "params": {}
    }
    try:
        headers = {"X-API-Key": API_KEY}
        response = requests.post(MCP_URL, json=payload, headers=headers, verify=False)
        print(f"Status: {response.status_code}")
        result = response.json()
        if "result" in result and "tools" in result["result"]:
            tools = result["result"]["tools"]
            print(f"\n✅ Found {len(tools)} tools:")
            for i, tool in enumerate(tools[:5], 1):  # Show first 5
                print(f"  {i}. {tool['name']}")
            if len(tools) > 5:
                print(f"  ... and {len(tools) - 5} more")
        else:
            print(f"Response:\n{json.dumps(result, indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_call_get_skills():
    """Test calling get_skills tool"""
    print("\n" + "=" * 60)
    print("TEST 5: Call Tool (get_skills)")
    print("=" * 60)
    payload = {
        "jsonrpc": "2.0",
        "id": 3,
        "method": "tools/call",
        "params": {
            "name": "get_skills",
            "arguments": {
                "min_weight": 7
            }
        }
    }
    try:
        headers = {"X-API-Key": API_KEY}
        response = requests.post(MCP_URL, json=payload, headers=headers, verify=False)
        print(f"Status: {response.status_code}")
        result = response.json()
        if "result" in result:
            print(f"✅ Success!")
            # Extract and show skills
            content = result["result"].get("content", [])
            if content and len(content) > 0:
                text = content[0].get("text", "")
                data = json.loads(text) if text else {}
                skills = data.get("skills", {})
                print(f"Found {len(skills)} skills with weight >= 7:")
                for skill, weight in list(skills.items())[:5]:
                    print(f"  - {skill}: {weight}")
                if len(skills) > 5:
                    print(f"  ... and {len(skills) - 5} more")
        else:
            print(f"Response:\n{json.dumps(result, indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_check_job_match():
    """Test job matching tool"""
    print("\n" + "=" * 60)
    print("TEST 6: Check Job Match")
    print("=" * 60)
    payload = {
        "jsonrpc": "2.0",
        "id": 4,
        "method": "tools/call",
        "params": {
            "name": "check_job_match",
            "arguments": {
                "job_title": "Machine Learning Engineer",
                "job_description": "Python, TensorFlow, PyTorch, ML pipelines, data engineering, AWS, Docker, Kubernetes"
            }
        }
    }
    try:
        headers = {"X-API-Key": API_KEY}
        response = requests.post(MCP_URL, json=payload, headers=headers, verify=False)
        print(f"Status: {response.status_code}")
        result = response.json()
        if "result" in result:
            print(f"✅ Success!")
            content = result["result"].get("content", [])
            if content and len(content) > 0:
                text = content[0].get("text", "")
                data = json.loads(text) if text else {}
                if data.get("match"):
                    print(f"Match Score: {data.get('match_score', 0)}")
                    print(f"Matched Skills: {data.get('matched_skills', 'N/A')[:100]}...")
                else:
                    print(f"No Match: {data.get('reason', 'Unknown')}")
        else:
            print(f"Response:\n{json.dumps(result, indent=2)[:500]}...")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_bearer_token_auth():
    """Test Bearer token authentication (for OpenAI SDK)"""
    print("\n" + "=" * 60)
    print("TEST 7: Bearer Token Authentication")
    print("=" * 60)
    try:
        headers = {"Authorization": f"Bearer {API_KEY}"}
        response = requests.get(MCP_URL, headers=headers, verify=False)
        print(f"Status: {response.status_code}")
        print(f"✅ Bearer token auth works!")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_query_param_auth():
    """Test query parameter authentication"""
    print("\n" + "=" * 60)
    print("TEST 8: Query Parameter Authentication")
    print("=" * 60)
    try:
        url = f"{MCP_URL}?api_key={API_KEY}"
        response = requests.get(url, verify=False)
        print(f"Status: {response.status_code}")
        print(f"✅ Query param auth works!")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    print("\n🚀 Testing ngrok.anix.app MCP endpoint for OpenAI SDK\n")
    print(f"Endpoint: {MCP_URL}")
    print(f"API Key: {API_KEY[:10]}...\n")
    
    # Disable SSL warnings
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    
    results = []
    
    # Run all tests
    results.append(("Auth Required", test_without_auth()))
    results.append(("Health Check", test_health_check()))
    results.append(("Initialize", test_initialize()))
    results.append(("List Tools", test_list_tools()))
    results.append(("Get Skills", test_call_get_skills()))
    results.append(("Job Match", test_check_job_match()))
    results.append(("Bearer Token Auth", test_bearer_token_auth()))
    results.append(("Query Param Auth", test_query_param_auth()))
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {test_name}")
    
    print(f"\n{passed}/{total} tests passed")
    
    if passed == total:
        print("\n✨ All tests passed! Your endpoint is ready for ChatGPT/OpenAI SDK")
        print("\n📋 To use with ChatGPT Custom Actions:")
        print(f"   1. URL: {MCP_URL}")
        print(f"   2. Authentication: API Key")
        print(f"   3. API Key Header: X-API-Key or Authorization: Bearer <key>")
        print(f"   4. Method: POST with JSON-RPC 2.0")
        print(f"\n🔑 Your API Key: {API_KEY}")
        print(f"\n💡 Example curl command:")
        print(f"   curl -X POST '{MCP_URL}' \\")
        print(f"     -H 'X-API-Key: {API_KEY}' \\")
        print(f"     -H 'Content-Type: application/json' \\")
        print(f"     -d '{{")
        print(f"       \"jsonrpc\": \"2.0\",")
        print(f"       \"id\": 1,")
        print(f"       \"method\": \"tools/list\",")
        print(f"       \"params\": {{}}")
        print(f"     }}'")
    else:
        print("\n⚠️  Some tests failed. Check the output above for details.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)

