# Quick Reference - ngrok.anix.app MCP Endpoint

## 🚀 Endpoint
```
https://anix.ngrok.app/mcp
```

## 🔑 Authentication
```
X-API-Key: owner-secret-key-change-me
```

## 📋 Quick Commands

### List all tools
```bash
curl -X POST https://anix.ngrok.app/mcp \
  -H "X-API-Key: owner-secret-key-change-me" \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/list","params":{}}'
```

### Get skills
```bash
curl -X POST https://anix.ngrok.app/mcp \
  -H "X-API-Key: owner-secret-key-change-me" \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"name":"get_skills","arguments":{"min_weight":7}}}'
```

### Check job match
```bash
curl -X POST https://anix.ngrok.app/mcp \
  -H "X-API-Key: owner-secret-key-change-me" \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":3,"method":"tools/call","params":{"name":"check_job_match","arguments":{"job_title":"ML Engineer","job_description":"Python TensorFlow AWS"}}}'
```

## 🛠️ All 14 Tools

| Tool | Description |
|------|-------------|
| `get_resume_info` | Full tech resume |
| `get_skills` | Filter skills by weight |
| `match_jobs` | Match jobs from DB |
| `get_shortlist` | Top matched jobs |
| `check_job_match` | Analyze single job |
| `get_b_past_life_resume_info` | VC/PE resume |
| `check_b_past_life_job_match` | Finance job match |
| `get_northstar_info` | Project overview |
| `list_projects` | All 5 projects |
| `get_project` | Project by ID |
| `get_project_by_name` | Project by name |
| `get_shared_assets` | Shared resources |
| `get_ai_agent_plan` | AI orchestration |
| `search_projects` | Keyword search |

## 🧪 Test
```bash
python3 test_with_auth.py
```

## 📖 Full Guides
- Setup: `CHATGPT_SETUP_GUIDE.md`
- OpenAPI: `openapi_chatgpt.yaml`
- Results: `TEST_RESULTS.md`

## ⚡ Server Control
```bash
# Start
python3 server_http.py &
ngrok http 8000 --domain=anix.ngrok.app

# Stop
pkill -f server_http
pkill ngrok
```

## 📊 Status: ✅ LIVE (8/8 tests passed)

