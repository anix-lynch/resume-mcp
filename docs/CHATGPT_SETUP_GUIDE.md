# ChatGPT Custom Actions Setup Guide

## ✅ Your Endpoint is Ready!

Your MCP endpoint at `https://anix.ngrok.app/mcp` is now fully compatible with ChatGPT Custom Actions and OpenAI SDK.

## 🔧 Setup Instructions for ChatGPT

### 1. Create a Custom GPT

1. Go to [ChatGPT](https://chat.openai.com)
2. Click your profile → "My GPTs"
3. Click "Create a GPT"
4. Go to "Configure" tab

### 2. Add Custom Action

In the Actions section:

**Schema Type:** OpenAPI 3.0

**Authentication:**
- Type: `API Key`
- Auth Type: `Custom`
- Header Name: `X-API-Key`
- API Key: `owner-secret-key-change-me`

**OpenAPI Schema:**

```yaml
openapi: 3.0.0
info:
  title: Resume MCP
  version: 1.0.0
  description: MCP server for resume querying, job matching, and project information
servers:
  - url: https://anix.ngrok.app
paths:
  /mcp:
    post:
      operationId: callMCPTool
      summary: Call an MCP tool
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                jsonrpc:
                  type: string
                  example: "2.0"
                id:
                  type: integer
                  example: 1
                method:
                  type: string
                  enum: [initialize, tools/list, tools/call]
                params:
                  type: object
                  properties:
                    name:
                      type: string
                      description: Tool name (for tools/call)
                    arguments:
                      type: object
                      description: Tool arguments (for tools/call)
      responses:
        '200':
          description: Success
          content:
            application/json:
              schema:
                type: object
```

### 3. Available Tools

Your MCP server provides **14 tools**:

#### Resume MCP Tools (Tech Resume)
1. **get_resume_info** - Full tech resume with skills, projects, experience
2. **get_skills** - Filter skills by weight (1-10)
3. **match_jobs** - Match and rank jobs from database
4. **get_shortlist** - Get top matched jobs
5. **check_job_match** - Check specific job match score

#### B Past Life MCP Tools (VC/PE/Finance Resume)
6. **get_b_past_life_resume_info** - VC/PE/Finance resume
7. **check_b_past_life_job_match** - Check job match for finance roles

#### Northstar MCP Tools (Project Registry)
8. **get_northstar_info** - Overview of all projects
9. **list_projects** - List all 5 Northstar projects
10. **get_project** - Get project by ID (1-5)
11. **get_project_by_name** - Get project by name
12. **get_shared_assets** - List shared assets
13. **get_ai_agent_plan** - AI agent orchestration plan
14. **search_projects** - Search projects by keyword

## 🧪 Test Your Setup

### Using curl:

```bash
# List all tools
curl -X POST 'https://anix.ngrok.app/mcp' \
  -H 'X-API-Key: owner-secret-key-change-me' \
  -H 'Content-Type: application/json' \
  -d '{
    "jsonrpc": "2.0",
    "id": 1,
    "method": "tools/list",
    "params": {}
  }'

# Get skills with weight >= 7
curl -X POST 'https://anix.ngrok.app/mcp' \
  -H 'X-API-Key: owner-secret-key-change-me' \
  -H 'Content-Type: application/json' \
  -d '{
    "jsonrpc": "2.0",
    "id": 2,
    "method": "tools/call",
    "params": {
      "name": "get_skills",
      "arguments": {"min_weight": 7}
    }
  }'

# Check job match
curl -X POST 'https://anix.ngrok.app/mcp' \
  -H 'X-API-Key: owner-secret-key-change-me' \
  -H 'Content-Type: application/json' \
  -d '{
    "jsonrpc": "2.0",
    "id": 3,
    "method": "tools/call",
    "params": {
      "name": "check_job_match",
      "arguments": {
        "job_title": "ML Engineer",
        "job_description": "Python, TensorFlow, AWS"
      }
    }
  }'
```

### Using Python:

```python
import requests

MCP_URL = "https://anix.ngrok.app/mcp"
API_KEY = "owner-secret-key-change-me"

def call_tool(tool_name, arguments=None):
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
    response = requests.post(MCP_URL, json=payload, headers=headers)
    return response.json()

# Get skills
result = call_tool("get_skills", {"min_weight": 8})
print(result)
```

## 📝 Example ChatGPT Prompts

Once your Custom GPT is set up, try these:

1. **"Show me my top technical skills"**
   - Uses: `get_skills` with min_weight=8

2. **"Does this job match my resume: [paste job description]"**
   - Uses: `check_job_match`

3. **"What are my Northstar projects?"**
   - Uses: `list_projects`

4. **"Tell me about my Resume MCP project"**
   - Uses: `get_project_by_name`

5. **"Check if I'm a good fit for this VC role: [description]"**
   - Uses: `check_b_past_life_job_match`

## 🔒 Security Notes

- **Current API Key:** `owner-secret-key-change-me` (change this!)
- Change the key by setting `OWNER_API_KEY` environment variable
- The endpoint supports:
  - Header: `X-API-Key: your-key`
  - Header: `Authorization: Bearer your-key`
  - Query param: `?api_key=your-key`

## 🚀 Server Management

**Start server + ngrok:**
```bash
# Start server
python3 server_http.py &

# Start ngrok
ngrok http 8000 --domain=anix.ngrok.app
```

**Check if running:**
```bash
curl -H "X-API-Key: owner-secret-key-change-me" https://anix.ngrok.app/mcp
```

**Run tests:**
```bash
python3 test_with_auth.py
```

## 📊 Response Format

All tools return JSON-RPC 2.0 responses:

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "content": [
      {
        "type": "text",
        "text": "{...actual data...}"
      }
    ]
  }
}
```

## 🎯 Next Steps

1. **Change API Key** - Set `OWNER_API_KEY` env var
2. **Create Custom GPT** - Follow setup instructions above
3. **Test with ChatGPT** - Try example prompts
4. **Monitor Usage** - Check ngrok dashboard for traffic

---

**Endpoint:** https://anix.ngrok.app/mcp  
**Status:** ✅ Live and tested  
**Protocol:** MCP (Model Context Protocol) via JSON-RPC 2.0  
**Tools Available:** 14 (Resume, B Past Life, Northstar)

