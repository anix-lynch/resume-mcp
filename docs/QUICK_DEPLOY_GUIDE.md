# Quick Deploy Guide

## 🐳 Docker (Local)

```bash
# Build and run
docker-compose up

# Or manually
docker build -t resume-mcp .
docker run -p 8000:8000 resume-mcp
```

## 🌐 Deploy as Real Website

### Railway (Recommended - Easiest)

1. **Push to GitHub** (if not already)
   ```bash
   git init
   git add .
   git commit -m "Resume MCP server"
   git remote add origin YOUR_GITHUB_REPO
   git push -u origin main
   ```

2. **Deploy on Railway:**
   - Go to: https://railway.app
   - Sign up with GitHub
   - "New Project" → "Deploy from GitHub repo"
   - Select your repo
   - Railway auto-detects Dockerfile
   - Click "Deploy"
   - Get URL: `yourname.railway.app`

3. **Add Custom Domain (Optional):**
   - Settings → Domains
   - Add: `resume.gozeroshot.dev`
   - Update DNS in your domain provider

**Done!** Your website runs 24/7, no ngrok needed!

### Render (Alternative)

1. Go to: https://render.com
2. "New" → "Web Service"
3. Connect GitHub repo
4. Build: `pip install -r requirements.txt`
5. Start: `python3 server_http.py`
6. Deploy!

## 💡 Comparison

**ngrok (Current):**
- ✅ Quick setup
- ✅ Works immediately
- ❌ Requires your computer running
- ❌ $10/month for static domain

**Real Website (Railway/Render):**
- ✅ Runs 24/7
- ✅ No computer needed
- ✅ Free tier available
- ✅ Custom domain included
- ✅ Professional setup

## 🎯 Recommendation

**For Production:** Deploy to Railway/Render
- Professional
- Always online
- Free tier available

**For Development:** Use ngrok
- Quick testing
- Easy local development
