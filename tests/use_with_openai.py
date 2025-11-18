#!/usr/bin/env python3
from openai import OpenAI
import requests

MCP_URL = "https://anix.ngrok.app/mcp"
API_KEY = "owner-secret-key-change-me"

def call_mcp_tool(tool_name, arguments=None):
    """Call MCP tool and return result"""
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/call",
        "params": {
            "name": tool_name,
            "arguments": arguments or {}
        }
    }
    headers = {"X-API-Key": API_KEY}
    response = requests.post(MCP_URL, json=payload, headers=headers, verify=False)
    result = response.json()
    if "result" in result:
        content = result["result"].get("content", [])
        if content:
            return content[0].get("text", "")
    return None

# Use with OpenAI
client = OpenAI(api_key="your-openai-api-key")

# Define MCP tools as OpenAI functions
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_resume_info",
            "description": "Get full tech resume information",
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_skills",
            "description": "Get skills filtered by weight",
            "parameters": {
                "type": "object",
                "properties": {
                    "min_weight": {"type": "integer", "description": "Minimum skill weight (1-10)"}
                }
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "check_job_match",
            "description": "Check job match score",
            "parameters": {
                "type": "object",
                "properties": {
                    "job_title": {"type": "string"},
                    "job_description": {"type": "string"}
                },
                "required": ["job_title", "job_description"]
            }
        }
    }
]

# Chat with function calling
response = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": "What are my top skills?"}],
    tools=tools,
    tool_choice="auto"
)

# Handle function calls
if response.choices[0].message.tool_calls:
    for tool_call in response.choices[0].message.tool_calls:
        tool_name = tool_call.function.name
        tool_args = eval(tool_call.function.arguments)
        result = call_mcp_tool(tool_name, tool_args)
        
        # Send result back to OpenAI
        client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "user", "content": "What are my top skills?"},
                response.choices[0].message,
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": result
                }
            ],
            tools=tools
        )

