# Deploy to Vercel

## 🎯 Quick Deploy

### Option 1: Vercel CLI (Recommended)

```bash
# Install Vercel CLI
npm i -g vercel

# Login
vercel login

# Deploy
vercel

# Deploy to production
vercel --prod
```

### Option 2: Vercel Dashboard

1. Go to: https://vercel.com
2. Sign up / Login
3. "Add New" → "Project"
4. Import your GitHub repo
5. Vercel auto-detects Python
6. Click "Deploy"
7. Get URL: `yourname.vercel.app`

## 📋 Configuration

I've created:
- ✅ `vercel.json` - Vercel config
- ✅ `api/index.py` - Serverless function adapter
- ✅ Updated `requirements.txt` - Added `mangum` for FastAPI

## ⚠️ Important Notes

**Vercel Limitations:**
- Serverless functions (10s timeout on free tier)
- File system is read-only (except `/tmp`)
- Need to bundle data files

**For Your Use Case:**
- ✅ API endpoints work great
- ✅ Web UI works
- ⚠️ File operations (CSV reading) might need adjustment
- ⚠️ Long-running operations might timeout

## 🔧 Adaptations Needed

If you have file operations, we might need to:
1. Use environment variables for data
2. Store CSV data in Vercel storage
3. Or use external storage (Supabase, S3)

## 💡 Recommendation

**For Vercel:**
- ✅ Great for API endpoints
- ✅ Web UI works perfectly
- ✅ Free tier
- ✅ Custom domain included
- ⚠️ Might need adjustments for file operations

**Alternative: Railway/Render**
- ✅ Better for long-running processes
- ✅ Full file system access
- ✅ No timeout limits

Want me to adapt the code for Vercel's serverless environment?
EOF
cat VERCEL_DEPLOY.md
