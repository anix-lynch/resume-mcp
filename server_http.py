#!/usr/bin/env python3
"""
MCP Server HTTP/SSE Endpoint for OpenAI Connector

This exposes the MCP server over HTTP with Server-Sent Events (SSE)
for OpenAI's connector interface.
"""

from fastapi import FastAPI, Request, Depends
from fastapi.responses import StreamingResponse, JSONResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
import json
import asyncio
from typing import Any, Dict
from pathlib import Path
from auth_middleware import require_auth, is_owner, require_owner

# Import matching functions directly
from match_rank import (
    load_resume,
    load_rulebook,
    match_and_rank,
    filter_jobs,
    rank_jobs
)
import pandas as pd

# Import B Past Life MCP functions
import sys
B_PAST_LIFE_DIR = Path(__file__).parent / "b_past_life_mcp"
B_PAST_LIFE_RESUME_FILE = B_PAST_LIFE_DIR / "resume.json"
B_PAST_LIFE_RULEBOOK_FILE = B_PAST_LIFE_DIR / "rulebook.yaml"

if str(B_PAST_LIFE_DIR) not in sys.path:
    sys.path.insert(0, str(B_PAST_LIFE_DIR))
try:
    # Import from b_past_life_mcp/match_rank.py
    import importlib.util
    spec = importlib.util.spec_from_file_location("b_past_life_match_rank", B_PAST_LIFE_DIR / "match_rank.py")
    b_past_life_match_rank = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(b_past_life_match_rank)
    
    # Create wrapper functions that use absolute paths
    def load_b_past_life_resume():
        """Load B Past Life resume from correct path."""
        with open(B_PAST_LIFE_RESUME_FILE, 'r') as f:
            return json.load(f)
    
    def load_b_past_life_rulebook():
        """Load B Past Life rulebook from correct path."""
        import yaml
        with open(B_PAST_LIFE_RULEBOOK_FILE, 'r') as f:
            return yaml.safe_load(f)
    
    b_past_life_match_and_rank = b_past_life_match_rank.match_and_rank
    b_past_life_filter_jobs = b_past_life_match_rank.filter_jobs
    b_past_life_rank_jobs = b_past_life_match_rank.rank_jobs
except Exception as e:
    print(f"Warning: Could not load B Past Life MCP functions: {e}")
    import traceback
    traceback.print_exc()
    load_b_past_life_resume = None
    load_b_past_life_rulebook = None
    b_past_life_filter_jobs = None
    b_past_life_rank_jobs = None

# Load Northstar projects data
NORTHSTAR_PROJECTS_FILE = Path(__file__).parent / "northstar_mcp" / "projects.json"

def load_northstar_projects():
    """Load Northstar projects data."""
    if NORTHSTAR_PROJECTS_FILE.exists():
        with open(NORTHSTAR_PROJECTS_FILE, 'r') as f:
            return json.load(f)
    return None

# Create FastAPI app for HTTP
http_app = FastAPI(title="Resume MCP HTTP Server", version="1.0.0")

# CORS for OpenAI connector
http_app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@http_app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    """Recruiter-friendly web interface (public access)."""
    # Public access allowed - no auth required for web UI
    resume = load_resume()
    if not resume:
        return HTMLResponse("<h1>Resume not found</h1>", status_code=404)
    
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>{resume.get('name', 'Resume')} - Interactive Resume</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            * {{ margin: 0; padding: 0; box-sizing: border-box; }}
            body {{
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                padding: 20px;
            }}
            .container {{
                max-width: 800px;
                margin: 0 auto;
                background: white;
                border-radius: 20px;
                box-shadow: 0 20px 60px rgba(0,0,0,0.3);
                overflow: hidden;
            }}
            .header {{
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 40px;
                text-align: center;
            }}
            .header h1 {{
                font-size: 2.5em;
                margin-bottom: 10px;
            }}
            .header p {{
                font-size: 1.2em;
                opacity: 0.9;
            }}
            .content {{
                padding: 40px;
            }}
            .query-section {{
                margin-bottom: 30px;
            }}
            .query-section h2 {{
                color: #333;
                margin-bottom: 20px;
                font-size: 1.5em;
            }}
            .query-buttons {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 15px;
                margin-bottom: 20px;
            }}
            button {{
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                border: none;
                padding: 15px 25px;
                border-radius: 10px;
                font-size: 1em;
                cursor: pointer;
                transition: transform 0.2s, box-shadow 0.2s;
            }}
            button:hover {{
                transform: translateY(-2px);
                box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
            }}
            .result {{
                background: #f8f9fa;
                border-radius: 10px;
                padding: 20px;
                margin-top: 20px;
                display: none;
            }}
            .result.show {{
                display: block;
            }}
            .result pre {{
                background: #2d2d2d;
                color: #f8f8f2;
                padding: 15px;
                border-radius: 5px;
                overflow-x: auto;
                font-size: 0.9em;
            }}
            .loading {{
                text-align: center;
                padding: 20px;
                color: #667eea;
            }}
            .info-section {{
                background: #f8f9fa;
                border-radius: 10px;
                padding: 20px;
                margin-top: 30px;
            }}
            .info-section h3 {{
                color: #333;
                margin-bottom: 15px;
            }}
            .info-section ul {{
                list-style: none;
                padding-left: 0;
            }}
            .info-section li {{
                padding: 8px 0;
                border-bottom: 1px solid #e0e0e0;
            }}
            .info-section li:last-child {{
                border-bottom: none;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>{resume.get('name', 'Resume')}</h1>
                <p>{resume.get('title', 'Professional Profile')}</p>
            </div>
            <div class="content">
                <div class="query-section">
                    <h2>🔍 Query Resume</h2>
                    <p style="margin-bottom: 20px; color: #666;">
                        Ask questions about skills, experience, projects, or check job matches.
                    </p>
                    <div class="query-buttons">
                        <button onclick="queryResume('get_resume_info')">📄 Full Resume</button>
                        <button onclick="queryResume('get_skills')">💼 Skills</button>
                        <button onclick="queryResume('get_shortlist')">⭐ Top Jobs</button>
                        <button onclick="checkJobMatch()">🎯 Check Job Match</button>
                    </div>
                    <div id="result" class="result"></div>
                </div>
                
                <div class="info-section">
                    <h3>📋 Quick Info</h3>
                    <ul>
                        <li><strong>Name:</strong> {resume.get('name', 'N/A')}</li>
                        <li><strong>Title:</strong> {resume.get('title', 'N/A')}</li>
                        <li><strong>Skills:</strong> {', '.join(list(resume.get('skills', {}).keys())[:5])}...</li>
                        <li><strong>Target Roles:</strong> {', '.join(resume.get('target_roles', [])[:3])}...</li>
                    </ul>
                </div>
            </div>
        </div>
        
        <script>
            async function queryResume(endpoint) {{
                const resultDiv = document.getElementById('result');
                resultDiv.innerHTML = '<div class="loading">⏳ Loading...</div>';
                resultDiv.classList.add('show');
                
                try {{
                    let url = `/api/${{endpoint}}`;
                    if (endpoint === 'get_skills') {{
                        url += '?min_weight=7';
                    }}
                    
                    const response = await fetch(url);
                    const data = await response.json();
                    
                    resultDiv.innerHTML = `
                        <h3>Result:</h3>
                        <pre>${{JSON.stringify(data, null, 2)}}</pre>
                    `;
                }} catch (error) {{
                    resultDiv.innerHTML = `
                        <h3>Error:</h3>
                        <pre>${{error.message}}</pre>
                    `;
                }}
            }}
            
            async function checkJobMatch() {{
                const jobTitle = prompt('Enter job title:');
                if (!jobTitle) return;
                
                const jobDesc = prompt('Enter job description:');
                if (!jobDesc) return;
                
                const resultDiv = document.getElementById('result');
                resultDiv.innerHTML = '<div class="loading">⏳ Checking match...</div>';
                resultDiv.classList.add('show');
                
                try {{
                    const response = await fetch('/api/check_job_match', {{
                        method: 'POST',
                        headers: {{ 'Content-Type': 'application/json' }},
                        body: JSON.stringify({{
                            job_title: jobTitle,
                            job_description: jobDesc
                        }})
                    }});
                    const data = await response.json();
                    
                    resultDiv.innerHTML = `
                        <h3>Job Match Result:</h3>
                        <pre>${{JSON.stringify(data, null, 2)}}</pre>
                    `;
                }} catch (error) {{
                    resultDiv.innerHTML = `
                        <h3>Error:</h3>
                        <pre>${{error.message}}</pre>
                    `;
                }}
            }}
        </script>
    </body>
    </html>
    """
    return HTMLResponse(html)

@http_app.get("/mcp")
@http_app.post("/mcp")
async def mcp_endpoint(request: Request):
    """
    MCP endpoint for OpenAI Connector handshake.
    Handles both GET (health check) and POST (JSON-RPC) requests.
    Initialize and tools/list work without auth; tools/call requires auth.
    """
    if request.method == "GET":
        # Health check - return server info (no auth needed)
        return JSONResponse({
            "protocol": "mcp",
            "version": "2024-11-05",
            "capabilities": {
                "tools": True,
                "resources": False,
                "prompts": False
            },
            "serverInfo": {
                "name": "resume-mcp",
                "version": "1.0.0"
            }
        })
    
    # POST request - handle JSON-RPC
    try:
        body = await request.json()
        
        # Handle initialize request (no auth needed for handshake)
        if body.get("method") == "initialize":
            return JSONResponse({
                "jsonrpc": "2.0",
                "id": body.get("id"),
                "result": {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {
                        "tools": {
                            "listChanged": True
                        }
                    },
                    "serverInfo": {
                        "name": "resume-mcp",
                        "version": "1.0.0"
                    }
                }
            })
        
        # Handle tools/list request (no auth needed)
        elif body.get("method") == "tools/list":
            # Combined tools from Resume MCP, B Past Life MCP, and Northstar MCP
            tools_list = [
                # Resume MCP tools (Tech Resume)
                {
                    "name": "get_resume_info",
                    "description": "Get full tech resume information including skills, projects, experience, and target roles",
                    "inputSchema": {
                        "type": "object",
                        "properties": {},
                    },
                },
                {
                    "name": "match_jobs",
                    "description": "Match and rank jobs from jobs_clean.csv against the tech resume. Returns top N matches.",
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
                    "description": "Get the current shortlist.csv (top matched jobs for tech resume)",
                    "inputSchema": {
                        "type": "object",
                        "properties": {},
                    },
                },
                {
                    "name": "get_skills",
                    "description": "Get skills from tech resume, optionally filtered by minimum weight",
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
                    "description": "Check how well a specific job description matches the tech resume",
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
                # B Past Life MCP tools (VC/PE/Finance Resume)
                {
                    "name": "get_b_past_life_resume_info",
                    "description": "Get B's past life resume (VC/PE/Finance) information including experience, skills, and achievements",
                    "inputSchema": {
                        "type": "object",
                        "properties": {},
                    },
                },
                {
                    "name": "check_b_past_life_job_match",
                    "description": "Check how well a job matches B's past life resume (VC/PE/Finance roles)",
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
                # Northstar MCP tools (Project Registry)
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
                "jsonrpc": "2.0",
                "id": body.get("id"),
                "result": {
                    "tools": tools_list
                }
            })
        
        # Handle tools/call request (no auth needed for ChatGPT connector)
        elif body.get("method") == "tools/call":
            
            params = body.get("params", {})
            tool_name = params.get("name")
            arguments = params.get("arguments", {})
            
            if not tool_name:
                return JSONResponse({
                    "jsonrpc": "2.0",
                    "id": body.get("id"),
                    "error": {
                        "code": -32602,
                        "message": "Invalid params: tool name required"
                    }
                })
            
            # Call the tool using the same logic as /call endpoint
            try:
                if tool_name == "get_resume_info":
                    resume = load_resume()
                    if not resume:
                        return JSONResponse({
                            "jsonrpc": "2.0",
                            "id": body.get("id"),
                            "error": {"code": -32000, "message": "Resume file not found"}
                        })
                    return JSONResponse({
                        "jsonrpc": "2.0",
                        "id": body.get("id"),
                        "result": {
                            "content": [
                                {
                                    "type": "text",
                                    "text": json.dumps(resume, indent=2)
                                }
                            ]
                        }
                    })
                
                elif tool_name == "get_skills":
                    resume = load_resume()
                    if not resume:
                        return JSONResponse({
                            "jsonrpc": "2.0",
                            "id": body.get("id"),
                            "error": {"code": -32000, "message": "Resume file not found"}
                        })
                    min_weight = arguments.get("min_weight", 0)
                    skills = {skill: weight for skill, weight in resume.get("skills", {}).items() if weight >= min_weight}
                    return JSONResponse({
                        "jsonrpc": "2.0",
                        "id": body.get("id"),
                        "result": {
                            "content": [
                                {
                                    "type": "text",
                                    "text": json.dumps({"skills": skills, "count": len(skills)}, indent=2)
                                }
                            ]
                        }
                    })
                
                elif tool_name == "match_jobs":
                    top_n = arguments.get("top_n", 5)
                    result = match_and_rank(top_n=top_n)
                    if isinstance(result, tuple):
                        success, shortlist_df, ranked_df = result
                        if success and shortlist_df is not None:
                            shortlist = shortlist_df.to_dict(orient="records")
                            return JSONResponse({
                                "jsonrpc": "2.0",
                                "id": body.get("id"),
                                "result": {
                                    "content": [
                                        {
                                            "type": "text",
                                            "text": json.dumps({"shortlist": shortlist, "count": len(shortlist)}, indent=2)
                                        }
                                    ]
                                }
                            })
                    return JSONResponse({
                        "jsonrpc": "2.0",
                        "id": body.get("id"),
                        "error": {"code": -32000, "message": "Failed to match jobs"}
                    })
                
                elif tool_name == "get_shortlist":
                    shortlist_file = Path("shortlist.csv")
                    if not shortlist_file.exists():
                        return JSONResponse({
                            "jsonrpc": "2.0",
                            "id": body.get("id"),
                            "error": {"code": -32000, "message": "Shortlist not found. Run match_jobs first."}
                        })
                    df = pd.read_csv(shortlist_file)
                    return JSONResponse({
                        "jsonrpc": "2.0",
                        "id": body.get("id"),
                        "result": {
                            "content": [
                                {
                                    "type": "text",
                                    "text": json.dumps({"shortlist": df.to_dict(orient="records"), "count": len(df)}, indent=2)
                                }
                            ]
                        }
                    })
                
                elif tool_name == "check_job_match":
                    resume = load_resume()
                    rulebook = load_rulebook()
                    if not resume or not rulebook:
                        return JSONResponse({
                            "jsonrpc": "2.0",
                            "id": body.get("id"),
                            "error": {"code": -32000, "message": "Resume or rulebook not found"}
                        })
                    
                    job_df = pd.DataFrame([{
                        "title": arguments.get("job_title", ""),
                        "company": arguments.get("company", ""),
                        "description": arguments.get("job_description", ""),
                        "url": ""
                    }])
                    
                    filtered_df, discarded_df = filter_jobs(job_df, rulebook)
                    if len(filtered_df) == 0:
                        result_data = {
                            "match": False,
                            "reason": "Job filtered out by rulebook",
                            "discard_reason": discarded_df.iloc[0].get("discard_reason", "Unknown") if len(discarded_df) > 0 else "No positive keyword matches"
                        }
                    else:
                        ranked_df = rank_jobs(filtered_df, resume, rulebook)
                        if len(ranked_df) > 0:
                            job_result = ranked_df.iloc[0].to_dict()
                            result_data = {
                                "match": True,
                                "match_score": job_result.get("match_score", 0),
                                "matched_skills": job_result.get("matched_skills", ""),
                                "matched_projects": job_result.get("matched_projects", ""),
                                "positive_keyword_matches": job_result.get("positive_keyword_matches", 0)
                            }
                        else:
                            return JSONResponse({
                                "jsonrpc": "2.0",
                                "id": body.get("id"),
                                "error": {"code": -32000, "message": "Failed to rank job"}
                            })
                    
                    return JSONResponse({
                        "jsonrpc": "2.0",
                        "id": body.get("id"),
                        "result": {
                            "content": [
                                {
                                    "type": "text",
                                    "text": json.dumps(result_data, indent=2)
                                }
                            ]
                        }
                    })
                
                # B Past Life MCP tools
                elif tool_name == "get_b_past_life_resume_info":
                    resume = load_b_past_life_resume()
                    if not resume:
                        return JSONResponse({
                            "jsonrpc": "2.0",
                            "id": body.get("id"),
                            "error": {"code": -32000, "message": "B Past Life resume file not found"}
                        })
                    return JSONResponse({
                        "jsonrpc": "2.0",
                        "id": body.get("id"),
                        "result": {
                            "content": [
                                {
                                    "type": "text",
                                    "text": json.dumps(resume, indent=2)
                                }
                            ]
                        }
                    })
                
                elif tool_name == "check_b_past_life_job_match":
                    resume = load_b_past_life_resume()
                    rulebook = load_b_past_life_rulebook()
                    if not resume or not rulebook:
                        return JSONResponse({
                            "jsonrpc": "2.0",
                            "id": body.get("id"),
                            "error": {"code": -32000, "message": "B Past Life resume or rulebook not found"}
                        })
                    
                    job_df = pd.DataFrame([{
                        "title": arguments.get("job_title", ""),
                        "company": arguments.get("company", ""),
                        "description": arguments.get("job_description", ""),
                        "url": ""
                    }])
                    
                    filtered_df, discarded_df = b_past_life_filter_jobs(job_df, rulebook)
                    if len(filtered_df) == 0:
                        result_data = {
                            "match": False,
                            "reason": "Job filtered out by rulebook",
                            "discard_reason": discarded_df.iloc[0].get("discard_reason", "Unknown") if len(discarded_df) > 0 else "No positive keyword matches"
                        }
                    else:
                        ranked_df = b_past_life_rank_jobs(filtered_df, resume, rulebook)
                        if len(ranked_df) > 0:
                            job_result = ranked_df.iloc[0].to_dict()
                            result_data = {
                                "match": True,
                                "match_score": job_result.get("match_score", 0),
                                "matched_skills": job_result.get("matched_skills", ""),
                                "matched_projects": job_result.get("matched_projects", ""),
                                "positive_keyword_matches": job_result.get("positive_keyword_matches", 0)
                            }
                        else:
                            return JSONResponse({
                                "jsonrpc": "2.0",
                                "id": body.get("id"),
                                "error": {"code": -32000, "message": "Failed to rank job"}
                            })
                    
                    return JSONResponse({
                        "jsonrpc": "2.0",
                        "id": body.get("id"),
                        "result": {
                            "content": [
                                {
                                    "type": "text",
                                    "text": json.dumps(result_data, indent=2)
                                }
                            ]
                        }
                    })
                
                # Northstar MCP tools
                elif tool_name == "get_northstar_info":
                    projects_data = load_northstar_projects()
                    if not projects_data:
                        return JSONResponse({
                            "jsonrpc": "2.0",
                            "id": body.get("id"),
                            "error": {"code": -32000, "message": "Northstar projects data not found"}
                        })
                    return JSONResponse({
                        "jsonrpc": "2.0",
                        "id": body.get("id"),
                        "result": {
                            "content": [
                                {
                                    "type": "text",
                                    "text": json.dumps({
                                        "brand": projects_data["brand"],
                                        "total_projects": projects_data["total_projects"],
                                        "mission": projects_data["mission"],
                                        "author": projects_data["meta"]["author"],
                                        "tone": projects_data["meta"]["tone"]
                                    }, indent=2)
                                }
                            ]
                        }
                    })
                
                elif tool_name == "list_projects":
                    projects_data = load_northstar_projects()
                    if not projects_data:
                        return JSONResponse({
                            "jsonrpc": "2.0",
                            "id": body.get("id"),
                            "error": {"code": -32000, "message": "Northstar projects data not found"}
                        })
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
                        "jsonrpc": "2.0",
                        "id": body.get("id"),
                        "result": {
                            "content": [
                                {
                                    "type": "text",
                                    "text": json.dumps({"projects": projects_list, "count": len(projects_list)}, indent=2)
                                }
                            ]
                        }
                    })
                
                elif tool_name == "get_project":
                    projects_data = load_northstar_projects()
                    if not projects_data:
                        return JSONResponse({
                            "jsonrpc": "2.0",
                            "id": body.get("id"),
                            "error": {"code": -32000, "message": "Northstar projects data not found"}
                        })
                    project_id = arguments.get("project_id")
                    if not project_id or project_id < 1 or project_id > 5:
                        return JSONResponse({
                            "jsonrpc": "2.0",
                            "id": body.get("id"),
                            "error": {"code": -32602, "message": "project_id must be between 1 and 5"}
                        })
                    
                    project = next((p for p in projects_data["projects"] if p["id"] == project_id), None)
                    if not project:
                        return JSONResponse({
                            "jsonrpc": "2.0",
                            "id": body.get("id"),
                            "error": {"code": -32000, "message": f"Project {project_id} not found"}
                        })
                    
                    return JSONResponse({
                        "jsonrpc": "2.0",
                        "id": body.get("id"),
                        "result": {
                            "content": [
                                {
                                    "type": "text",
                                    "text": json.dumps(project, indent=2)
                                }
                            ]
                        }
                    })
                
                elif tool_name == "get_project_by_name":
                    projects_data = load_northstar_projects()
                    if not projects_data:
                        return JSONResponse({
                            "jsonrpc": "2.0",
                            "id": body.get("id"),
                            "error": {"code": -32000, "message": "Northstar projects data not found"}
                        })
                    project_name = arguments.get("project_name", "").lower()
                    if not project_name:
                        return JSONResponse({
                            "jsonrpc": "2.0",
                            "id": body.get("id"),
                            "error": {"code": -32602, "message": "project_name is required"}
                        })
                    
                    matching = [
                        p for p in projects_data["projects"]
                        if project_name in p["name"].lower()
                    ]
                    
                    if not matching:
                        return JSONResponse({
                            "jsonrpc": "2.0",
                            "id": body.get("id"),
                            "error": {"code": -32000, "message": f"No project found matching '{project_name}'"}
                        })
                    
                    return JSONResponse({
                        "jsonrpc": "2.0",
                        "id": body.get("id"),
                        "result": {
                            "content": [
                                {
                                    "type": "text",
                                    "text": json.dumps(matching[0] if len(matching) == 1 else matching, indent=2)
                                }
                            ]
                        }
                    })
                
                elif tool_name == "get_shared_assets":
                    projects_data = load_northstar_projects()
                    if not projects_data:
                        return JSONResponse({
                            "jsonrpc": "2.0",
                            "id": body.get("id"),
                            "error": {"code": -32000, "message": "Northstar projects data not found"}
                        })
                    return JSONResponse({
                        "jsonrpc": "2.0",
                        "id": body.get("id"),
                        "result": {
                            "content": [
                                {
                                    "type": "text",
                                    "text": json.dumps({
                                        "shared_assets": projects_data["shared_assets"],
                                        "count": len(projects_data["shared_assets"])
                                    }, indent=2)
                                }
                            ]
                        }
                    })
                
                elif tool_name == "get_ai_agent_plan":
                    projects_data = load_northstar_projects()
                    if not projects_data:
                        return JSONResponse({
                            "jsonrpc": "2.0",
                            "id": body.get("id"),
                            "error": {"code": -32000, "message": "Northstar projects data not found"}
                        })
                    return JSONResponse({
                        "jsonrpc": "2.0",
                        "id": body.get("id"),
                        "result": {
                            "content": [
                                {
                                    "type": "text",
                                    "text": json.dumps(projects_data["ai_agent_plan"], indent=2)
                                }
                            ]
                        }
                    })
                
                elif tool_name == "search_projects":
                    projects_data = load_northstar_projects()
                    if not projects_data:
                        return JSONResponse({
                            "jsonrpc": "2.0",
                            "id": body.get("id"),
                            "error": {"code": -32000, "message": "Northstar projects data not found"}
                        })
                    keyword = arguments.get("keyword", "").lower()
                    if not keyword:
                        return JSONResponse({
                            "jsonrpc": "2.0",
                            "id": body.get("id"),
                            "error": {"code": -32602, "message": "keyword is required"}
                        })
                    
                    matching = []
                    for project in projects_data["projects"]:
                        search_text = f"{project['name']} {project['purpose']} {' '.join(project['stack'])} {project['mcp_role']}".lower()
                        if keyword in search_text:
                            matching.append(project)
                    
                    return JSONResponse({
                        "jsonrpc": "2.0",
                        "id": body.get("id"),
                        "result": {
                            "content": [
                                {
                                    "type": "text",
                                    "text": json.dumps({
                                        "projects": matching,
                                        "count": len(matching),
                                        "keyword": keyword
                                    }, indent=2)
                                }
                            ]
                        }
                    })
                
                else:
                    return JSONResponse({
                        "jsonrpc": "2.0",
                        "id": body.get("id"),
                        "error": {
                            "code": -32601,
                            "message": f"Unknown tool: {tool_name}"
                        }
                    })
            
            except Exception as e:
                return JSONResponse({
                    "jsonrpc": "2.0",
                    "id": body.get("id"),
                    "error": {
                        "code": -32000,
                        "message": f"Tool execution error: {str(e)}"
                    }
                })
        
        # Default response for other methods
        return JSONResponse({
            "jsonrpc": "2.0",
            "id": body.get("id"),
            "error": {
                "code": -32601,
                "message": "Method not found"
            }
        })
        
    except Exception as e:
        return JSONResponse({
            "jsonrpc": "2.0",
            "id": None,
            "error": {
                "code": -32700,
                "message": f"Parse error: {str(e)}"
            }
        }, status_code=400)

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

@http_app.get("/api/get_resume_info")
async def api_get_resume_info(request: Request):
    """API endpoint for full resume (for web UI). Requires auth (owner has automatic)."""
    require_auth(request, allow_public=False)
    resume = load_resume()
    if not resume:
        return JSONResponse({"error": "Resume not found"}, status_code=404)
    return JSONResponse(resume)

@http_app.get("/api/get_skills")
async def api_get_skills(request: Request, min_weight: int = 0):
    """API endpoint for skills (for web UI). Requires auth (owner has automatic)."""
    require_auth(request, allow_public=False)
    resume = load_resume()
    if not resume:
        return JSONResponse({"error": "Resume not found"}, status_code=404)
    skills = resume.get('skills', {})
    filtered = {k: v for k, v in skills.items() if v >= min_weight}
    return JSONResponse({"skills": filtered, "count": len(filtered)})

@http_app.get("/api/get_shortlist")
async def api_get_shortlist(request: Request):
    """API endpoint for job shortlist (for web UI). Requires auth (owner has automatic)."""
    require_auth(request, allow_public=False)
    try:
        result = match_and_rank(top_n=5)
        if isinstance(result, tuple):
            success, shortlist_df, ranked_df = result
            if success and shortlist_df is not None:
                return JSONResponse({
                    "shortlist": shortlist_df.to_dict(orient="records"),
                    "count": len(shortlist_df)
                })
        return JSONResponse({"error": "No shortlist available"}, status_code=404)
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)

@http_app.post("/api/check_job_match")
async def api_check_job_match(request: Request):
    """API endpoint for job matching (for web UI). Requires auth (owner has automatic)."""
    require_auth(request, allow_public=False)
    try:
        data = await request.json()
        job_df = pd.DataFrame([{
            "title": data.get("job_title", ""),
            "company": data.get("company", ""),
            "description": data.get("job_description", ""),
            "url": ""
        }])
        
        rulebook = load_rulebook()
        filtered_df, discarded_df = filter_jobs(job_df, rulebook)
        if len(filtered_df) == 0:
            return JSONResponse({
                "match": False,
                "reason": "Job filtered out by rulebook"
            })
        
        resume = load_resume()
        ranked_df = rank_jobs(filtered_df, resume, rulebook)
        if len(ranked_df) > 0:
            job_result = ranked_df.iloc[0].to_dict()
            return JSONResponse({
                "match": True,
                "match_score": job_result.get("match_score", 0),
                "matched_skills": job_result.get("matched_skills", ""),
                "matched_projects": job_result.get("matched_projects", "")
            })
        
        return JSONResponse({"error": "Failed to rank job"}, status_code=500)
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)

@http_app.get("/tools")
async def get_tools(request: Request):
    """Get list of available MCP tools (combined from all MCPs). Requires auth (owner has automatic)."""
    require_auth(request, allow_public=False)
    # Combined tools from Resume MCP, B Past Life MCP, and Northstar MCP
    tools_list = [
        # Resume MCP tools (Tech Resume)
        {
            "name": "get_resume_info",
            "description": "Get full tech resume information including skills, projects, experience, and target roles",
            "inputSchema": {"type": "object", "properties": {}},
        },
        {
            "name": "match_jobs",
            "description": "Match and rank jobs from jobs_clean.csv against the tech resume. Returns top N matches.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "top_n": {"type": "integer", "description": "Number of top jobs to return (default: 5)", "default": 5},
                },
            },
        },
        {
            "name": "get_shortlist",
            "description": "Get the current shortlist.csv (top matched jobs for tech resume)",
            "inputSchema": {"type": "object", "properties": {}},
        },
        {
            "name": "get_skills",
            "description": "Get skills from tech resume, optionally filtered by minimum weight",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "min_weight": {"type": "integer", "description": "Minimum skill weight to include (1-10)", "default": 0},
                },
            },
        },
        {
            "name": "check_job_match",
            "description": "Check how well a specific job description matches the tech resume",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "job_title": {"type": "string", "description": "Job title"},
                    "job_description": {"type": "string", "description": "Job description text"},
                    "company": {"type": "string", "description": "Company name (optional)", "default": ""},
                },
                "required": ["job_title", "job_description"],
            },
        },
        # B Past Life MCP tools
        {
            "name": "get_b_past_life_resume_info",
            "description": "Get B's past life resume (VC/PE/Finance) information including experience, skills, and achievements",
            "inputSchema": {"type": "object", "properties": {}},
        },
        {
            "name": "check_b_past_life_job_match",
            "description": "Check how well a job matches B's past life resume (VC/PE/Finance roles)",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "job_title": {"type": "string", "description": "Job title"},
                    "job_description": {"type": "string", "description": "Job description text"},
                    "company": {"type": "string", "description": "Company name (optional)", "default": ""},
                },
                "required": ["job_title", "job_description"],
            },
        },
        # Northstar MCP tools
        {
            "name": "get_northstar_info",
            "description": "Get overview of Northstar suite including brand, mission, and total projects",
            "inputSchema": {"type": "object", "properties": {}},
        },
        {
            "name": "list_projects",
            "description": "List all 5 Northstar projects with basic information",
            "inputSchema": {"type": "object", "properties": {}},
        },
        {
            "name": "get_project",
            "description": "Get detailed information about a specific project by ID (1-5)",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "project_id": {"type": "integer", "description": "Project ID (1-5)"},
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
                    "project_name": {"type": "string", "description": "Project name or partial name"},
                },
                "required": ["project_name"],
            },
        },
        {
            "name": "get_shared_assets",
            "description": "Get list of shared assets across all Northstar projects",
            "inputSchema": {"type": "object", "properties": {}},
        },
        {
            "name": "get_ai_agent_plan",
            "description": "Get AI agent orchestration plan (short-term and long-term)",
            "inputSchema": {"type": "object", "properties": {}},
        },
        {
            "name": "search_projects",
            "description": "Search projects by keyword in name, purpose, stack, or MCP role",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "keyword": {"type": "string", "description": "Search keyword"},
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
    """Call an MCP tool via HTTP. Requires auth (owner has automatic)."""
    # Require auth (owner gets automatic auth via Vercel SSO or API key)
    require_auth(request, allow_public=False)
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
        
        # B Past Life MCP tools
        elif tool_name == "get_b_past_life_resume_info":
            if not load_b_past_life_resume:
                return JSONResponse({"error": "B Past Life MCP not available"}, status_code=503)
            resume = load_b_past_life_resume()
            if not resume:
                return JSONResponse({"error": "B Past Life resume file not found"}, status_code=404)
            return JSONResponse({"result": resume})
        
        elif tool_name == "check_b_past_life_job_match":
            if not load_b_past_life_resume or not load_b_past_life_rulebook:
                return JSONResponse({"error": "B Past Life MCP not available"}, status_code=503)
            resume = load_b_past_life_resume()
            rulebook = load_b_past_life_rulebook()
            if not resume or not rulebook:
                return JSONResponse({"error": "B Past Life resume or rulebook not found"}, status_code=500)
            
            job_df = pd.DataFrame([{
                "title": arguments.get("job_title", ""),
                "company": arguments.get("company", ""),
                "description": arguments.get("job_description", ""),
                "url": ""
            }])
            
            filtered_df, discarded_df = b_past_life_filter_jobs(job_df, rulebook)
            if len(filtered_df) == 0:
                return JSONResponse({
                    "result": {
                        "match": False,
                        "reason": "Job filtered out by rulebook",
                        "discard_reason": discarded_df.iloc[0].get("discard_reason", "Unknown") if len(discarded_df) > 0 else "No positive keyword matches"
                    }
                })
            
            ranked_df = b_past_life_rank_jobs(filtered_df, resume, rulebook)
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
        
        # Northstar MCP tools
        elif tool_name == "get_northstar_info":
            projects_data = load_northstar_projects()
            if not projects_data:
                return JSONResponse({"error": "Northstar projects data not found"}, status_code=404)
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
            projects_data = load_northstar_projects()
            if not projects_data:
                return JSONResponse({"error": "Northstar projects data not found"}, status_code=404)
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
            projects_data = load_northstar_projects()
            if not projects_data:
                return JSONResponse({"error": "Northstar projects data not found"}, status_code=404)
            project_id = arguments.get("project_id")
            if not project_id or project_id < 1 or project_id > 5:
                return JSONResponse({"error": "project_id must be between 1 and 5"}, status_code=400)
            
            project = next((p for p in projects_data["projects"] if p["id"] == project_id), None)
            if not project:
                return JSONResponse({"error": f"Project {project_id} not found"}, status_code=404)
            
            return JSONResponse({"result": project})
        
        elif tool_name == "get_project_by_name":
            projects_data = load_northstar_projects()
            if not projects_data:
                return JSONResponse({"error": "Northstar projects data not found"}, status_code=404)
            project_name = arguments.get("project_name", "").lower()
            if not project_name:
                return JSONResponse({"error": "project_name is required"}, status_code=400)
            
            matching = [
                p for p in projects_data["projects"]
                if project_name in p["name"].lower()
            ]
            
            if not matching:
                return JSONResponse({"error": f"No project found matching '{project_name}'"}, status_code=404)
            
            return JSONResponse({
                "result": matching[0] if len(matching) == 1 else matching,
                "count": len(matching)
            })
        
        elif tool_name == "get_shared_assets":
            projects_data = load_northstar_projects()
            if not projects_data:
                return JSONResponse({"error": "Northstar projects data not found"}, status_code=404)
            return JSONResponse({
                "result": {
                    "shared_assets": projects_data["shared_assets"],
                    "count": len(projects_data["shared_assets"])
                }
            })
        
        elif tool_name == "get_ai_agent_plan":
            projects_data = load_northstar_projects()
            if not projects_data:
                return JSONResponse({"error": "Northstar projects data not found"}, status_code=404)
            return JSONResponse({"result": projects_data["ai_agent_plan"]})
        
        elif tool_name == "search_projects":
            projects_data = load_northstar_projects()
            if not projects_data:
                return JSONResponse({"error": "Northstar projects data not found"}, status_code=404)
            keyword = arguments.get("keyword", "").lower()
            if not keyword:
                return JSONResponse({"error": "keyword is required"}, status_code=400)
            
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
            return JSONResponse({"error": f"Unknown tool: {tool_name}"}, status_code=400)
        
    except Exception as e:
        return JSONResponse(
            {"error": str(e)},
            status_code=500
        )

if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting Resume MCP HTTP Server on http://localhost:8000")
    print("📡 MCP endpoint: http://localhost:8000/mcp")
    print("📡 SSE endpoint: http://localhost:8000/sse")
    print("🔧 Tools endpoint: http://localhost:8000/tools")
    print("\n💡 Use ngrok to expose this server:")
    print("   ngrok http 8000")
    print("\n📋 For OpenAI Connector, use:")
    print("   https://YOUR-NGROK-URL.ngrok-free.app/mcp")
    uvicorn.run(http_app, host="0.0.0.0", port=8000)

