# Recruiter Interface - Share Your Resume as a Link/QR Code

## 🎯 What This Does

Instead of sending a PDF resume, you can share:
- ✅ **A link** (e.g., `yourname.ngrok-free.app`)
- ✅ **A QR code** (scan → access resume)
- ✅ **Interactive interface** (recruiters can query your resume)

## 🚀 Quick Start

### Option 1: Use Your Existing MCP Server (Recommended)

Your MCP server already has all the data! Just add a web interface route.

### Option 2: Standalone Recruiter Interface

1. **Start the interface:**
   ```bash
   ./start_recruiter_interface.sh
   ```

2. **Expose with ngrok:**
   ```bash
   ngrok http 8001
   ```

3. **Get your public URL:**
   - Copy the ngrok URL (e.g., `https://abc123.ngrok-free.app`)
   - Or use your static domain if you have one

4. **Generate QR code:**
   ```bash
   python3 generate_qr_code.py https://your-url.ngrok-free.app
   ```

5. **Share:**
   - Put QR code on business card
   - Add link to email signature
   - Share in LinkedIn profile

## 📋 What Recruiters Can Do

- **View Full Resume** - All your info
- **Check Skills** - See your skill set
- **View Top Job Matches** - See what jobs match you
- **Check Job Match** - Enter a job description, see match score

## 💡 Integration with Static Domain

If you have ngrok static domain:
1. Use same domain for both MCP and recruiter interface
2. Set up subdomain or different port
3. Or integrate recruiter interface into main server

## 🎨 Customization

Edit `recruiter_interface.py` to:
- Change colors/styling
- Add more query options
- Customize the interface
