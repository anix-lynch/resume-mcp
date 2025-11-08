#!/usr/bin/env python3
"""
Northstar MCP Server - Project Registry & Architecture

Exposes tools for querying Northstar project information, architecture,
and project status.
"""

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import StreamingResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import json
import asyncio
from pathlib import Path
from typing import Any, Optional

# Load projects data
PROJECTS_FILE = Path(__file__).parent / "projects.json"

def load_projects():
    """Load projects data."""
    with open(PROJECTS_FILE, 'r') as f:
        return json.load(f)

# Create FastAPI app
http_app = FastAPI(title="Northstar MCP Server", version="1.0.0")

# CORS for OpenAI connector
http_app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@http_app.get("/")
async def root():
    """Health check endpoint."""
    return {
        "name": "Northstar MCP Server",
        "version": "1.0.0",
        "status": "running",
        "description": "Project registry and architecture information for Northstar suite",
        "endpoints": {
            "mcp": "/mcp",
            "sse": "/sse",
            "tools": "/tools",
            "call": "/call"
        }
    }

@http_app.get("/mcp")
@http_app.post("/mcp")
async def mcp_endpoint():
    """
    MCP endpoint for OpenAI Connector handshake.
    This is the main endpoint ChatGPT uses to connect.
    """
    return JSONResponse({
        "protocol": "mcp",
        "version": "2024-11-05",
        "capabilities": {
            "tools": True,
            "resources": False,
            "prompts": False
        },
        "serverInfo": {
            "name": "northstar-mcp",
            "version": "1.0.0"
        }
    })

@http_app.get("/sse")
async def sse_endpoint(request: Request):
    """
    SSE endpoint for OpenAI connector.
    """
    async def event_stream():
        try:
            yield f"data: {json.dumps({'type': 'connection', 'status': 'connected'})}\n\n"
            while True:
                await asyncio.sleep(1)
                yield f"data: {json.dumps({'type': 'ping'})}\n\n"
        except asyncio.CancelledError:
            yield f"data: {json.dumps({'type': 'connection', 'status': 'disconnected'})}\n\n"
    
    return StreamingResponse(
        event_stream(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"
        }
    )

@http_app.get("/tools")
async def get_tools():
    """Get list of available MCP tools."""
    tools_list = [
        {
            "name": "get_northstar_info",
            "description": "Get overview of Northstar suite including brand, mission, and total projects",
            "inputSchema": {
                "type": "object",
                "properties": {},
            },
        },
        {
            "name": "list_projects",
            "description": "List all 5 Northstar projects with basic information",
            "inputSchema": {
                "type": "object",
                "properties": {},
            },
        },
        {
            "name": "get_project",
            "description": "Get detailed information about a specific project by ID (1-5)",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "project_id": {
                        "type": "integer",
                        "description": "Project ID (1-5)",
                    },
                },
                "required": ["project_id"],
            },
        },
        {
            "name": "get_project_by_name",
            "description": "Get project information by name (e.g., 'Resume MCP', 'Mocktailverse')",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "project_name": {
                        "type": "string",
                        "description": "Project name or partial name",
                    },
                },
                "required": ["project_name"],
            },
        },
        {
            "name": "get_shared_assets",
            "description": "Get list of shared assets across all Northstar projects",
            "inputSchema": {
                "type": "object",
                "properties": {},
            },
        },
        {
            "name": "get_ai_agent_plan",
            "description": "Get AI agent orchestration plan (short-term and long-term)",
            "inputSchema": {
                "type": "object",
                "properties": {},
            },
        },
        {
            "name": "search_projects",
            "description": "Search projects by keyword in name, purpose, stack, or MCP role",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "keyword": {
                        "type": "string",
                        "description": "Search keyword",
                    },
                },
                "required": ["keyword"],
            },
        },
    ]
    return JSONResponse({
        "tools": tools_list,
        "count": len(tools_list)
    })

@http_app.post("/call")
async def call_tool_endpoint(request: Request):
    """Call an MCP tool via HTTP."""
    try:
        body = await request.json()
        tool_name = body.get("name")
        arguments = body.get("arguments", {})
        
        if not tool_name:
            return JSONResponse(
                {"error": "Tool name is required"},
                status_code=400
            )
        
        projects_data = load_projects()
        
        if tool_name == "get_northstar_info":
            return JSONResponse({
                "result": {
                    "brand": projects_data["brand"],
                    "total_projects": projects_data["total_projects"],
                    "mission": projects_data["mission"],
                    "author": projects_data["meta"]["author"],
                    "tone": projects_data["meta"]["tone"]
                }
            })
        
        elif tool_name == "list_projects":
            projects_list = [
                {
                    "id": p["id"],
                    "name": p["name"],
                    "purpose": p["purpose"],
                    "stack": p["stack"],
                    "mcp_role": p["mcp_role"]
                }
                for p in projects_data["projects"]
            ]
            return JSONResponse({
                "result": {
                    "projects": projects_list,
                    "count": len(projects_list)
                }
            })
        
        elif tool_name == "get_project":
            project_id = arguments.get("project_id")
            if not project_id or project_id < 1 or project_id > 5:
                return JSONResponse(
                    {"error": "project_id must be between 1 and 5"},
                    status_code=400
                )
            
            project = next((p for p in projects_data["projects"] if p["id"] == project_id), None)
            if not project:
                return JSONResponse(
                    {"error": f"Project {project_id} not found"},
                    status_code=404
                )
            
            return JSONResponse({"result": project})
        
        elif tool_name == "get_project_by_name":
            project_name = arguments.get("project_name", "").lower()
            if not project_name:
                return JSONResponse(
                    {"error": "project_name is required"},
                    status_code=400
                )
            
            matching = [
                p for p in projects_data["projects"]
                if project_name in p["name"].lower()
            ]
            
            if not matching:
                return JSONResponse(
                    {"error": f"No project found matching '{project_name}'"},
                    status_code=404
                )
            
            return JSONResponse({
                "result": matching[0] if len(matching) == 1 else matching,
                "count": len(matching)
            })
        
        elif tool_name == "get_shared_assets":
            return JSONResponse({
                "result": {
                    "shared_assets": projects_data["shared_assets"],
                    "count": len(projects_data["shared_assets"])
                }
            })
        
        elif tool_name == "get_ai_agent_plan":
            return JSONResponse({
                "result": projects_data["ai_agent_plan"]
            })
        
        elif tool_name == "search_projects":
            keyword = arguments.get("keyword", "").lower()
            if not keyword:
                return JSONResponse(
                    {"error": "keyword is required"},
                    status_code=400
                )
            
            matching = []
            for project in projects_data["projects"]:
                search_text = f"{project['name']} {project['purpose']} {' '.join(project['stack'])} {project['mcp_role']}".lower()
                if keyword in search_text:
                    matching.append(project)
            
            return JSONResponse({
                "result": {
                    "projects": matching,
                    "count": len(matching),
                    "keyword": keyword
                }
            })
        
        else:
            return JSONResponse(
                {"error": f"Unknown tool: {tool_name}"},
                status_code=400
            )
        
    except Exception as e:
        return JSONResponse(
            {"error": str(e)},
            status_code=500
        )

if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting Northstar MCP HTTP Server on http://localhost:8002")
    print("📡 MCP endpoint: http://localhost:8002/mcp")
    print("📡 SSE endpoint: http://localhost:8002/sse")
    print("🔧 Tools endpoint: http://localhost:8002/tools")
    print("\n💡 Use ngrok to expose this server:")
    print("   ngrok http 8002")
    print("\n📋 For OpenAI Connector, use:")
    print("   https://YOUR-NGROK-URL.ngrok-free.app/mcp")
    uvicorn.run(http_app, host="0.0.0.0", port=8002)

