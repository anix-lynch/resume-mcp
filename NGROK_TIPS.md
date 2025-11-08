# ngrok URL Management Tips

## Why ngrok URL Changes

ngrok **free tier** generates a **random URL** each time you restart it:
- Restart ngrok = New URL
- Must update ChatGPT connector = Annoying! 😤

## ✅ Solution: Keep ngrok Running!

**Best practice:** Only restart the Python server, keep ngrok running.

### Quick Commands:

```bash
# First time: Start everything
./start_resume_mcp.sh

# When you change code: Restart server only (keeps ngrok URL!)
./restart_server_only.sh

# Only stop everything when you're done
./stop_resume_mcp.sh
```

## How It Works

1. **`start_resume_mcp.sh`**: 
   - Starts Python server
   - Starts ngrok (only if not already running)
   - ✅ **Checks if ngrok is already running** - keeps existing tunnel!

2. **`restart_server_only.sh`**:
   - Restarts only Python server
   - Keeps ngrok running
   - ✅ **URL stays the same!**

3. **`stop_resume_mcp.sh`**:
   - Stops both server and ngrok
   - Use when you're done for the day

## Alternative Solutions

### Option 1: ngrok Static Domain (Paid)
- ngrok paid plan (~$8/month)
- Get a static domain like `yourname.ngrok-free.app`
- URL never changes

### Option 2: Keep ngrok Running Forever
- Run ngrok in a separate terminal
- Never stop it
- Only restart Python server when needed

### Option 3: Use ngrok Config File
```yaml
# ngrok.yml
version: "2"
authtoken: YOUR_TOKEN
tunnels:
  resume_mcp:
    proto: http
    addr: 8000
    # Add domain if you have paid plan
    # domain: yourname.ngrok-free.app
```

Then run: `ngrok start resume_mcp --config ngrok.yml`

## Current URL

Check your current URL:
```bash
cat ngrok_url.txt
```

Or:
```bash
curl -s http://localhost:4040/api/tunnels | jq -r '.tunnels[0].public_url'
```
