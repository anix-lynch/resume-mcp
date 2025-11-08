#!/usr/bin/env python3
"""
MCP Server HTTP/SSE Endpoint for OpenAI Connector

This exposes the MCP server over HTTP with Server-Sent Events (SSE)
for OpenAI's connector interface.
"""

from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import json
import asyncio
from typing import Any, Dict
from pathlib import Path

# Import matching functions directly
from match_rank import (
    load_resume,
    load_rulebook,
    match_and_rank,
    filter_jobs,
    rank_jobs
)
import pandas as pd

# Create FastAPI app for HTTP
http_app = FastAPI(title="B Past Life MCP HTTP Server", version="1.0.0")

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
        "name": "B Past Life MCP Server",
        "version": "1.0.0",
        "status": "running",
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
            "name": "b-past-life-mcp",
            "version": "1.0.0"
        }
    })

@http_app.get("/sse")
async def sse_endpoint(request: Request):
    """
    SSE endpoint for OpenAI connector.
    This is the main endpoint OpenAI will connect to.
    """
    async def event_stream():
        try:
            # Send initial connection message
            yield f"data: {json.dumps({'type': 'connection', 'status': 'connected'})}\n\n"
            
            # Keep connection alive and handle requests
            while True:
                # In a real implementation, you'd parse SSE messages from the client
                # For now, we'll keep the connection alive
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
            "name": "get_resume_info",
            "description": "Get full resume information including skills, projects, experience, and target roles",
            "inputSchema": {
                "type": "object",
                "properties": {},
            },
        },
        {
            "name": "match_jobs",
            "description": "Match and rank jobs from jobs_clean.csv against the resume. Returns top N matches.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "top_n": {
                        "type": "integer",
                        "description": "Number of top jobs to return (default: 5)",
                        "default": 5,
                    },
                },
            },
        },
        {
            "name": "get_shortlist",
            "description": "Get the current shortlist.csv (top matched jobs)",
            "inputSchema": {
                "type": "object",
                "properties": {},
            },
        },
        {
            "name": "get_skills",
            "description": "Get skills from resume, optionally filtered by minimum weight",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "min_weight": {
                        "type": "integer",
                        "description": "Minimum skill weight to include (1-10)",
                        "default": 0,
                    },
                },
            },
        },
        {
            "name": "check_job_match",
            "description": "Check how well a specific job description matches the resume",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "job_title": {
                        "type": "string",
                        "description": "Job title",
                    },
                    "job_description": {
                        "type": "string",
                        "description": "Job description text",
                    },
                    "company": {
                        "type": "string",
                        "description": "Company name (optional)",
                        "default": "",
                    },
                },
                "required": ["job_title", "job_description"],
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
        
        # Call the appropriate tool
        if tool_name == "get_resume_info":
            resume = load_resume()
            if not resume:
                return JSONResponse({"error": "Resume file not found"}, status_code=404)
            return JSONResponse({"result": resume})
        
        elif tool_name == "match_jobs":
            top_n = arguments.get("top_n", 5)
            result = match_and_rank(top_n=top_n)
            if isinstance(result, tuple):
                success, shortlist_df, ranked_df = result
                if success and shortlist_df is not None:
                    shortlist = shortlist_df.to_dict(orient="records")
                    return JSONResponse({"result": {"shortlist": shortlist, "count": len(shortlist)}})
            return JSONResponse({"error": "Failed to match jobs"}, status_code=500)
        
        elif tool_name == "get_shortlist":
            shortlist_file = Path("shortlist.csv")
            if not shortlist_file.exists():
                return JSONResponse({"error": "Shortlist not found. Run match_jobs first."}, status_code=404)
            df = pd.read_csv(shortlist_file)
            return JSONResponse({"result": {"shortlist": df.to_dict(orient="records"), "count": len(df)}})
        
        elif tool_name == "get_skills":
            resume = load_resume()
            if not resume:
                return JSONResponse({"error": "Resume file not found"}, status_code=404)
            min_weight = arguments.get("min_weight", 0)
            skills = {skill: weight for skill, weight in resume.get("skills", {}).items() if weight >= min_weight}
            return JSONResponse({"result": {"skills": skills, "count": len(skills)}})
        
        elif tool_name == "check_job_match":
            resume = load_resume()
            rulebook = load_rulebook()
            if not resume or not rulebook:
                return JSONResponse({"error": "Resume or rulebook not found"}, status_code=500)
            
            job_df = pd.DataFrame([{
                "title": arguments.get("job_title", ""),
                "company": arguments.get("company", ""),
                "description": arguments.get("job_description", ""),
                "url": ""
            }])
            
            filtered_df, discarded_df = filter_jobs(job_df, rulebook)
            if len(filtered_df) == 0:
                return JSONResponse({
                    "result": {
                        "match": False,
                        "reason": "Job filtered out by rulebook",
                        "discard_reason": discarded_df.iloc[0].get("discard_reason", "Unknown") if len(discarded_df) > 0 else "No positive keyword matches"
                    }
                })
            
            ranked_df = rank_jobs(filtered_df, resume, rulebook)
            if len(ranked_df) > 0:
                job_result = ranked_df.iloc[0].to_dict()
                return JSONResponse({
                    "result": {
                        "match": True,
                        "match_score": job_result.get("match_score", 0),
                        "matched_skills": job_result.get("matched_skills", ""),
                        "matched_projects": job_result.get("matched_projects", ""),
                        "positive_keyword_matches": job_result.get("positive_keyword_matches", 0)
                    }
                })
            return JSONResponse({"error": "Failed to rank job"}, status_code=500)
        
        else:
            return JSONResponse({"error": f"Unknown tool: {tool_name}"}, status_code=400)
        
    except Exception as e:
        return JSONResponse(
            {"error": str(e)},
            status_code=500
        )

if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting B Past Life MCP HTTP Server on http://localhost:8001")
    print("📡 MCP endpoint: http://localhost:8001/mcp")
    print("📡 SSE endpoint: http://localhost:8001/sse")
    print("🔧 Tools endpoint: http://localhost:8001/tools")
    print("\n💡 Use ngrok to expose this server:")
    print("   ngrok http 8001")
    print("\n📋 For OpenAI Connector, use:")
    print("   https://YOUR-NGROK-URL.ngrok-free.app/mcp")
    uvicorn.run(http_app, host="0.0.0.0", port=8001)

