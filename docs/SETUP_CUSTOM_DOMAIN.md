# Setup Custom Domain: anixlynch.com

## 🎯 Goal
Use your custom domain `anixlynch.com` (from Google Domains) with ngrok instead of the free dev domain.

## 📋 Step-by-Step

### Step 1: Add Custom Domain in ngrok Dashboard

1. In ngrok dashboard, click **"+ New Domain"** button
2. Choose **"Custom Domain"** option
3. Enter your domain:
   - Option A: Use subdomain (recommended): `resume.anixlynch.com` or `mcp.anixlynch.com`
   - Option B: Use root domain: `anixlynch.com` (requires special setup)
4. Click **"Create"** or **"Add"**
5. ngrok will show you DNS instructions

### Step 2: Get DNS CNAME Record from ngrok

After adding domain, ngrok will show you:
- **CNAME Record** to create (e.g., `resume.anixlynch.com`)
- **Points to:** (e.g., `abc123.ngrok-free.app` or similar)
- **Copy this information!**

### Step 3: Add DNS Record in Google Domains

1. Go to: https://domains.google.com
2. Select your domain: `anixlynch.com`
3. Go to **"DNS"** section
4. Click **"Custom resource records"** or **"DNS"**
5. Add new CNAME record:
   - **Name:** `resume` (or `mcp`, or leave blank for root)
   - **Type:** `CNAME`
   - **Data:** (paste the value ngrok gave you)
   - **TTL:** 3600 (or default)
6. Click **"Add"** or **"Save"**

### Step 4: Wait for DNS Propagation

- DNS changes take 5-60 minutes to propagate
- You can check with: `nslookup resume.anixlynch.com`

### Step 5: Verify in ngrok

- Go back to ngrok dashboard
- Your domain should show as "Active" or "Verified"
- Status should be green/active

### Step 6: Use in Your Scripts

Once verified, your domain will be:
- `https://resume.anixlynch.com` (if using subdomain)
- Or `https://anixlynch.com` (if using root)

## 💡 Recommendation

**Use a subdomain** (e.g., `resume.anixlynch.com`):
- ✅ Easier to set up
- ✅ Doesn't affect your main website
- ✅ Can use root domain for other things
- ✅ Professional looking

## 🚀 After Setup

I'll update your scripts to use:
- `resume.anixlynch.com` (or whatever you choose)
- Same setup process, just different domain!
