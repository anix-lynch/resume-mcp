# B Past Life MCP

**Separate MCP for pre-tech era resume (VC/PE/Finance/Real Estate)**

This is an isolated MCP server for testing rulebook matching with your past life resume (2019 CV) before integrating with your current tech resume.

## 🎯 Purpose

- Test rulebook.yaml with VC/PE/Finance domain
- Keep separate from current tech resume
- Different domain focus (VC/PE vs Tech)
- Isolated testing environment

## 📁 Structure

```
b_past_life_mcp/
├── resume.json          # VC/PE/Finance resume (2019)
├── rulebook.yaml        # VC/PE/Finance keywords
├── match_rank.py        # Matching logic
├── server_http.py       # HTTP server (port 8001)
└── README.md            # This file
```

## 🚀 Quick Start

```bash
cd b_past_life_mcp

# Start server (different port to avoid conflict)
python3 server_http.py

# In another terminal, expose with ngrok
ngrok http 8001
```

## 🔧 Configuration

- **Port:** 8001 (to avoid conflict with main MCP on 8000)
- **Resume:** VC/PE/Finance focused (2019)
- **Rulebook:** VC/PE/Finance keywords (excludes tech-only roles)

## 📋 Resume Focus

- Venture Capital / Private Equity
- Fund Management
- Real Estate Investment
- Strategic Planning
- Ecosystem Building
- Cross-border Strategy

## 🚫 Excluded

- Tech-only roles (software engineer, developer, etc.)
- This is intentionally separate from tech resume

## 🔗 OpenAI Connector

Use the ngrok URL with `/sse` endpoint:
```
https://YOUR-NGROK-URL.ngrok-free.app/sse
```

**Name:** `B Past Life MCP`
**Description:** `VC/PE/Finance resume matching (pre-tech era)`

---

**Status:** Isolated from main tech resume MCP

