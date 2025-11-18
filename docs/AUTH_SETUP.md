# 🔐 Authentication Setup

## ✅ What's Configured

**Automatic Auth for You:**
- Via Vercel SSO (if deployment protection enabled)
- Via Owner API Key (set in environment)

**Required Auth for Others:**
- Public API Key required
- Can be passed via header, query param, or cookie

## 🎯 How It Works

### For You (Owner):
1. **Vercel SSO** (if deployment protection ON):
   - Automatically authenticated when logged into Vercel
   - No API key needed

2. **Owner API Key** (if deployment protection OFF):
   - Set `OWNER_API_KEY` in environment
   - Use in requests: `X-API-Key: YOUR_OWNER_KEY`

### For Others:
- Must provide `PUBLIC_API_KEY` in requests
- Methods:
  - Header: `X-API-Key: PUBLIC_KEY`
  - Query: `?api_key=PUBLIC_KEY`
  - Cookie: `api_key=PUBLIC_KEY`

## 📋 Setup Steps

### 1. Generate API Keys

```bash
./setup_auth.sh
```

This creates `.env` with:
- `OWNER_API_KEY` - Your private key
- `PUBLIC_API_KEY` - Share with others

### 2. Add to Vercel Environment Variables

1. Go to: https://vercel.com/anix-lynchs-projects/01_resume_mcp
2. Settings → Environment Variables
3. Add:
   - `OWNER_API_KEY` = (from .env)
   - `PUBLIC_API_KEY` = (from .env)
4. Redeploy

### 3. Choose Authentication Method

**Option A: Vercel SSO (Recommended)**
- Keep deployment protection ON
- You're auto-authenticated
- Others need API key

**Option B: API Keys Only**
- Turn deployment protection OFF
- Everyone uses API keys
- You use OWNER_API_KEY
- Others use PUBLIC_API_KEY

## 🔧 Usage Examples

### For You (Owner):

```bash
# With Vercel SSO (deployment protection ON)
curl https://01resumemcp.vercel.app/mcp

# With Owner API Key
curl -H "X-API-Key: YOUR_OWNER_KEY" https://01resumemcp.vercel.app/mcp
```

### For Others:

```bash
# Via Header
curl -H "X-API-Key: PUBLIC_KEY" https://01resumemcp.vercel.app/mcp

# Via Query
curl "https://01resumemcp.vercel.app/mcp?api_key=PUBLIC_KEY"

# Via Cookie
curl -H "Cookie: api_key=PUBLIC_KEY" https://01resumemcp.vercel.app/mcp
```

## 🌐 Web UI

- **Public Access**: Web UI (`/`) is public (no auth needed)
- **API Endpoints**: All `/api/*` endpoints require auth

## 🔒 Security Notes

- Keep `OWNER_API_KEY` secret
- Share `PUBLIC_API_KEY` only with trusted users
- Rotate keys periodically
- Use HTTPS (Vercel provides this)

## 🎯 Endpoints

**Public (No Auth):**
- `GET /` - Web UI

**Protected (Auth Required):**
- `GET/POST /mcp` - MCP endpoint
- `GET /tools` - List tools
- `POST /call` - Call tool
- `GET /api/*` - All API endpoints

EOF
cat AUTH_SETUP.md
