# ngrok Purchase & Setup Guide

## Step 1: Purchase ngrok Plan

1. Go to: https://ngrok.com/pricing
2. Click "Get Started" on the **Personal** plan ($10/month)
3. Sign up / Log in
4. Complete payment
5. You'll get access to the dashboard

## Step 2: Get Your Static Domain

1. Go to ngrok dashboard: https://dashboard.ngrok.com
2. Navigate to **Domains** section
3. Click **Reserve Domain** or **Add Domain**
4. Choose a domain name (e.g., `anix-resume`)
5. Your static domain will be: `anix-resume.ngrok-free.app`
6. **Copy this domain name!**

## Step 3: Set Up Static Domain Locally

Once you have your domain, run:

```bash
# Set your static domain
export NGROK_STATIC_DOMAIN=your-domain.ngrok-free.app

# Start server with static domain
./start_resume_mcp_static.sh
```

Or add to your shell config (permanent):

```bash
# Add to ~/.zshrc or ~/.bashrc
echo 'export NGROK_STATIC_DOMAIN=your-domain.ngrok-free.app' >> ~/.zshrc
source ~/.zshrc
```

## Step 4: Update ChatGPT

1. Go to ChatGPT → Settings → Apps & Connectors
2. Update your connector URL to:
   `https://your-domain.ngrok-free.app/mcp`
3. **Never update again!** 🎉

## Step 5: Test

```bash
# Test your static domain
curl https://your-domain.ngrok-free.app/mcp
```

## Quick Setup Script

After purchase, just run:

```bash
# 1. Set your domain (replace with your actual domain)
export NGROK_STATIC_DOMAIN=your-domain.ngrok-free.app

# 2. Start server
./start_resume_mcp_static.sh

# 3. Copy the URL shown and update ChatGPT
```

That's it! Your URL will never change again.
