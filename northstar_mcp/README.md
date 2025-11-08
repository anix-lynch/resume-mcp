# Northstar MCP

**Project Registry & Architecture MCP**

This MCP server exposes information about the Northstar suite of 5 interoperable projects.

## 🎯 Purpose

- Query Northstar project information
- Get architecture details
- Search projects by keyword
- Access shared assets and AI agent plans

## 📁 Structure

```
northstar_mcp/
├── projects.json        # Northstar project registry
├── server_http.py       # HTTP server (port 8002)
└── README.md            # This file
```

## 🚀 Quick Start

```bash
cd northstar_mcp

# Start server
python3 server_http.py

# In another terminal, expose with ngrok
ngrok http 8002
```

## 🔧 Available Tools

- `get_northstar_info` - Get overview (brand, mission, total projects)
- `list_projects` - List all 5 projects with basic info
- `get_project` - Get detailed info by project ID (1-5)
- `get_project_by_name` - Get project by name
- `get_shared_assets` - List shared assets across projects
- `get_ai_agent_plan` - Get AI orchestration plan
- `search_projects` - Search projects by keyword

## 📋 Projects

1. **Resume MCP** - Core intelligence layer for job matching
2. **Mocktailverse** - AWS ETL pipeline
3. **Cocktailverse** - GCP ETL pipeline
4. **Dynamic Resume** - Full-stack visualization
5. **Marketing Analytics Dashboard** - ETL + Visualization

## 🔗 OpenAI Connector

Use the ngrok URL with `/sse` endpoint:
```
https://YOUR-NGROK-URL.ngrok-free.app/sse
```

**Name:** `Northstar MCP`
**Description:** `Project registry and architecture for Northstar suite`

---

**Status:** Separate MCP for project documentation

