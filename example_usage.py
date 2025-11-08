#!/usr/bin/env python3
"""
Example: Using your MCP server from any Python app
(Not just OpenAI SDK!)
"""

import requests
import json

# Your MCP server URL (with static domain, this never changes!)
MCP_URL = "https://YOUR-NGROK-URL.ngrok-free.app/mcp"

def call_mcp_tool(tool_name, arguments=None):
    """Call any MCP tool from your server."""
    if arguments is None:
        arguments = {}
    
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/call",
        "params": {
            "name": tool_name,
            "arguments": arguments
        }
    }
    
    response = requests.post(MCP_URL, json=payload)
    return response.json()

# Example: Get resume info
print("Calling get_resume_info...")
result = call_mcp_tool("get_resume_info")
print(json.dumps(result, indent=2))

# Example: Get skills
print("\nCalling get_skills...")
result = call_mcp_tool("get_skills", {"min_weight": 8})
print(json.dumps(result, indent=2))

# Example: Check job match
print("\nCalling check_job_match...")
result = call_mcp_tool("check_job_match", {
    "job_title": "Data Engineer",
    "job_description": "Python, ML, Data Engineering"
})
print(json.dumps(result, indent=2))
