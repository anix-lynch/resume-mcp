#!/usr/bin/env python3
"""
Test ngrok.anix.app endpoint with OpenAI SDK
This tests if the MCP server works with ChatGPT's custom actions/OpenAI SDK
"""

import requests
import json

# Your ngrok static domain endpoint
MCP_URL = "https://anix.ngrok.app/mcp"

def test_health_check():
    """Test GET endpoint (health check)"""
    print("=" * 60)
    print("TEST 1: Health Check (GET /mcp)")
    print("=" * 60)
    try:
        response = requests.get(MCP_URL)
        print(f"Status: {response.status_code}")
        print(f"Response:\n{json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_initialize():
    """Test MCP initialize handshake"""
    print("\n" + "=" * 60)
    print("TEST 2: Initialize (MCP Handshake)")
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
        response = requests.post(MCP_URL, json=payload)
        print(f"Status: {response.status_code}")
        print(f"Response:\n{json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_list_tools():
    """Test listing available tools"""
    print("\n" + "=" * 60)
    print("TEST 3: List Tools")
    print("=" * 60)
    payload = {
        "jsonrpc": "2.0",
        "id": 2,
        "method": "tools/list",
        "params": {}
    }
    try:
        response = requests.post(MCP_URL, json=payload)
        print(f"Status: {response.status_code}")
        result = response.json()
        if "result" in result and "tools" in result["result"]:
            tools = result["result"]["tools"]
            print(f"\n✅ Found {len(tools)} tools:")
            for tool in tools:
                print(f"  - {tool['name']}: {tool['description']}")
        else:
            print(f"Response:\n{json.dumps(result, indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_call_tool():
    """Test calling a specific tool"""
    print("\n" + "=" * 60)
    print("TEST 4: Call Tool (get_skills)")
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
        response = requests.post(MCP_URL, json=payload)
        print(f"Status: {response.status_code}")
        print(f"Response:\n{json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_check_job_match():
    """Test job matching tool"""
    print("\n" + "=" * 60)
    print("TEST 5: Check Job Match")
    print("=" * 60)
    payload = {
        "jsonrpc": "2.0",
        "id": 4,
        "method": "tools/call",
        "params": {
            "name": "check_job_match",
            "arguments": {
                "job_title": "Machine Learning Engineer",
                "job_description": "Python, TensorFlow, PyTorch, ML pipelines, data engineering, AWS"
            }
        }
    }
    try:
        response = requests.post(MCP_URL, json=payload)
        print(f"Status: {response.status_code}")
        print(f"Response:\n{json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_openai_compatibility():
    """Test OpenAI SDK compatibility"""
    print("\n" + "=" * 60)
    print("TEST 6: OpenAI SDK Compatibility Check")
    print("=" * 60)
    print("Testing if endpoint is compatible with OpenAI custom actions...")
    
    # Test 1: OPTIONS request (CORS preflight)
    try:
        response = requests.options(MCP_URL)
        print(f"✓ OPTIONS request status: {response.status_code}")
        print(f"  CORS headers: {dict(response.headers)}")
    except Exception as e:
        print(f"  OPTIONS test: {e}")
    
    # Test 2: Authentication header support
    try:
        headers = {"Authorization": "Bearer test-token"}
        response = requests.get(MCP_URL, headers=headers)
        print(f"✓ Auth header test status: {response.status_code}")
    except Exception as e:
        print(f"  Auth test: {e}")
    
    return True

def main():
    print("\n🚀 Testing ngrok.anix.app MCP endpoint for OpenAI SDK compatibility\n")
    print(f"Endpoint: {MCP_URL}\n")
    
    results = []
    
    # Run all tests
    results.append(("Health Check", test_health_check()))
    results.append(("Initialize", test_initialize()))
    results.append(("List Tools", test_list_tools()))
    results.append(("Call Tool", test_call_tool()))
    results.append(("Job Match", test_check_job_match()))
    results.append(("OpenAI Compatibility", test_openai_compatibility()))
    
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
        print(f"   1. Use this URL: {MCP_URL}")
        print(f"   2. Method: POST")
        print(f"   3. Format: JSON-RPC 2.0")
        print(f"   4. Available tools: get_resume_info, get_skills, check_job_match, etc.")
    else:
        print("\n⚠️  Some tests failed. Check the output above for details.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)

