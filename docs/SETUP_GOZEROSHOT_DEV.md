# Setup gozeroshot.dev for Resume MCP

## 🎯 Goal
Use `gozeroshot.dev` domain for your resume MCP (you have a Vercel project there, but we'll use a subdomain)

## 📋 Step-by-Step

### Step 1: Add Domain in ngrok Dashboard

1. In ngrok dashboard, click **"+ New Domain"**
2. Choose **"Custom Domain"**
3. Enter subdomain: **`resume.gozeroshot.dev`**
   - This keeps your Vercel project at `gozeroshot.dev` working
   - Resume MCP at `resume.gozeroshot.dev`
4. Click **"Create"**
5. ngrok will show DNS instructions - **copy them!**

### Step 2: Add DNS Record in Your Domain Provider

**If gozeroshot.dev is on:**
- **Vercel:** Add DNS record in Vercel dashboard
- **Google Domains:** Add in Google Domains DNS
- **Other:** Add in your domain provider's DNS

**Add CNAME record:**
- **Name:** `resume`
- **Type:** `CNAME`
- **Data:** (paste what ngrok gives you)
- **TTL:** 3600 (or default)

### Step 3: Wait for DNS Propagation
- Takes 5-60 minutes
- Check: `nslookup resume.gozeroshot.dev`

### Step 4: Verify in ngrok
- Domain should show as "Active" in ngrok dashboard

### Step 5: I'll Update Everything
Once verified, I'll:
- ✅ Update all scripts to use `resume.gozeroshot.dev`
- ✅ Set up server
- ✅ Give you final URLs

## 💡 Result

- `gozeroshot.dev` → Your Vercel project (unchanged)
- `resume.gozeroshot.dev` → Resume MCP (new!)

Perfect separation! 🎉
