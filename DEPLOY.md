# Deployment Guide

## Before Deploying

### 1. Set Environment Variables

**Local (.env file):**
```bash
cp env.example .env
# Edit .env with your actual keys
```

**Required:**
- `OWNER_API_KEY` - Your secure API key
- `PUBLIC_API_KEY` - Public API key (optional)

**Optional:**
- `NGROK_STATIC_DOMAIN` - Your ngrok static domain
- `GEMINI_API_KEY` - For langchain features
- `VERCEL_BYPASS_SECRET` - For Vercel deployment protection

### 2. Verify .gitignore

These files are **NOT** committed:
- `.env` files
- `*.log` files
- `*.db` files
- `ngrok_url.txt`
- Database files in `data/`

## Deploy to Vercel

1. **Install Vercel CLI:**
```bash
npm i -g vercel
```

2. **Set Environment Variables in Vercel Dashboard:**
   - Go to your project → Settings → Environment Variables
   - Add: `OWNER_API_KEY`, `PUBLIC_API_KEY`, etc.

3. **Deploy:**
```bash
vercel --prod
```

**Note:** The `api/index.py` file handles FastAPI → Vercel adapter automatically.

## Deploy to GitHub

1. **Check what will be committed:**
```bash
git status
```

2. **Verify sensitive files are ignored:**
```bash
git check-ignore .env docs/*.log data/*.db
```

3. **Commit and push:**
```bash
git add .
git commit -m "Organized repo structure"
git push origin main
```

## What's Safe to Commit

✅ **Safe:**
- All Python code
- Configuration files (vercel.json, requirements.txt)
- Documentation in `docs/`
- Test files
- Data files (CSV) - if you want them public

❌ **NOT Safe (already in .gitignore):**
- `.env` files
- Log files
- Database files
- API keys in code (use env vars instead)

## Current Security

- ✅ Default API keys in `auth_middleware.py` are **fallbacks only**
- ✅ Production should use environment variables
- ✅ `.gitignore` excludes all sensitive files
- ✅ No hardcoded production secrets

## Quick Deploy Checklist

- [ ] Copy `env.example` to `.env` and fill values
- [ ] Set env vars in Vercel dashboard (if deploying)
- [ ] Verify `.gitignore` excludes sensitive files
- [ ] Test locally: `python3 server_http.py`
- [ ] Deploy: `vercel --prod` or push to GitHub

