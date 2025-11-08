# Step-by-Step: Get Your ngrok Static Domain

## 🎯 What I Need From You

Your ngrok static domain (e.g., `anix-resume.ngrok-free.app`)

## 📋 Step-by-Step Instructions

### Step 1: Go to ngrok Dashboard
1. Open your browser
2. Go to: **https://dashboard.ngrok.com**
3. Log in with your account (the one you used for $10/month subscription)

### Step 2: Navigate to Domains
1. Look at the **left sidebar**
2. Click on **"Domains"** (or "Cloud Edge" → "Domains")
3. You should see a list of domains

### Step 3: Check if You Already Have a Domain
- If you see a domain listed (e.g., `yourname.ngrok-free.app`):
  - ✅ **Copy that domain name** - that's what I need!
  - Skip to Step 5

- If you see "No domains" or empty list:
  - Continue to Step 4

### Step 4: Reserve a New Domain (if needed)
1. Click **"Reserve Domain"** or **"Add Domain"** button
2. Enter a domain name (e.g., `anix-resume`)
   - Keep it short and memorable
   - Only letters, numbers, and hyphens
   - No spaces or special characters
3. Click **"Reserve"** or **"Create"**
4. Your domain will be: `yourname.ngrok-free.app`
5. ✅ **Copy that domain name** - that's what I need!

### Step 5: Share the Domain With Me
Just tell me the domain name, for example:
- `anix-resume.ngrok-free.app`
- `resume-mcp.ngrok-free.app`
- `anixlynch.ngrok-free.app`

## 🔍 Alternative: Check via Command Line

If you prefer, you can also check via terminal:

```bash
# Check if ngrok is running and get domain
curl -s http://localhost:4040/api/tunnels | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    tunnels = data.get('tunnels', [])
    for tunnel in tunnels:
        if 'domain' in tunnel.get('config', {}).get('addr', ''):
            print('Domain:', tunnel.get('public_url', ''))
        else:
            print('Tunnel URL:', tunnel.get('public_url', ''))
except:
    print('ngrok not running or no tunnels')
"
```

## 📸 What to Look For

In the ngrok dashboard, you'll see something like:

```
┌─────────────────────────────────────┐
│ Domains                             │
├─────────────────────────────────────┤
│ anix-resume.ngrok-free.app          │
│ Status: Active                       │
│ Created: 2024-01-15                  │
└─────────────────────────────────────┘
```

## ⚠️ Troubleshooting

**Can't find Domains section?**
- Look for "Cloud Edge" → "Domains"
- Or "Settings" → "Domains"
- Or check the top navigation menu

**Don't see Reserve Domain button?**
- Make sure you're on the paid plan ($10/month)
- Check your subscription status
- Contact ngrok support if needed

**Domain already reserved but can't find it?**
- Check "All Domains" or "Reserved Domains" tab
- Look in different sections of dashboard

## ✅ Once You Have It

Just tell me:
- The domain name (e.g., `anix-resume.ngrok-free.app`)

And I'll:
- ✅ Set it up permanently
- ✅ Start your server
- ✅ Give you the ChatGPT URL
- ✅ Set up recruiter interface
- ✅ Generate QR code

That's it! 🎉
