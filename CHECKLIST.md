# 📋 Resume MCP Deployment Checklist

**Goal:** Deploy Resume MCP to Vercel with authentication, connect to ChatGPT, and share with recruiters.

---

## ✅ Phase 1: Vercel Deployment

### 1.1 Add API Keys to Vercel Environment Variables
- [ ] **(b turn)** Go to: https://vercel.com/anix-lynchs-projects/01_resume_mcp
- [ ] **(b turn)** Click **Settings** → **Environment Variables**
- [ ] **(b turn)** Click **Add New**
- [ ] **(b turn)** Add first variable:
  - **Key:** `OWNER_API_KEY`
  - **Value:** `f91aab4749d6f8dcc7b91d8d983278fa8b9b4ba6944cf4c0a21632f6395b7115`
  - **Environment:** Select **Production** (and Preview if you want)
  - Click **Save**
- [ ] **(b turn)** Click **Add New** again
- [ ] **(b turn)** Add second variable:
  - **Key:** `PUBLIC_API_KEY`
  - **Value:** `128438458c46cec459439b2adddca362db36b6e48bfe4e608d3ba1e25c5f32f4`
  - **Environment:** Select **Production** (and Preview if you want)
  - Click **Save**
- [ ] **(b turn)** Verify both variables appear in the list

### 1.2 Redeploy to Vercel
- [ ] **(b turn)** Go to **Deployments** tab
- [ ] **(b turn)** Find the latest deployment (top of list)
- [ ] **(b turn)** Click the **three dots (⋯)** menu on that deployment
- [ ] **(b turn)** Click **Redeploy**
- [ ] **(b turn)** Wait for deployment to complete (watch the status)
- [ ] **(b turn)** Confirm status shows **"Ready"** (green checkmark)

### 1.3 Disable Deployment Protection
- [ ] **(b turn)** Go to **Settings** → **Deployment Protection**
- [ ] **(b turn)** Find **"Enable Deployment Protection"** toggle
- [ ] **(b turn)** Toggle it to **OFF**
- [ ] **(b turn)** Click **Save** (if there's a save button)
- [ ] **(b turn)** Confirm the toggle is now OFF

### 1.4 Verify URLs Work
- [ ] **(b turn)** Open browser, go to: `https://01resumemcp.vercel.app/`
- [ ] **(b turn)** Confirm you see the resume web interface (not an error)
- [ ] **(b turn)** Open new tab, go to: `https://01resumemcp.vercel.app/mcp`
- [ ] **(b turn)** Confirm you see JSON response (not an error page)

---

## ✅ Phase 2: Authentication Setup

### 2.1 Understand Authentication
- [ ] **(b turn)** Read: You get automatic auth via Vercel SSO (if protection ON) or use OWNER_API_KEY
- [ ] **(b turn)** Read: Others must use PUBLIC_API_KEY in requests
- [ ] **(b turn)** Read: Web UI (`/`) is public (no auth needed)

### 2.2 Test Owner Authentication (Optional)
- [ ] **(b turn)** Open terminal
- [ ] **(b turn)** Run: `curl -H "X-API-Key: f91aab4749d6f8dcc7b91d8d983278fa8b9b4ba6944cf4c0a21632f6395b7115" https://01resumemcp.vercel.app/mcp`
- [ ] **(b turn)** Confirm you get JSON response (not error)
- [ ] **(b turn)** Run: `curl https://01resumemcp.vercel.app/mcp` (without key)
- [ ] **(b turn)** Confirm you get error (401 Unauthorized)

### 2.3 Test Public Authentication (Optional)
- [ ] **(b turn)** Run: `curl -H "X-API-Key: 128438458c46cec459439b2adddca362db36b6e48bfe4e608d3ba1e25c5f32f4" https://01resumemcp.vercel.app/mcp`
- [ ] **(b turn)** Confirm you get JSON response (not error)

---

## ✅ Phase 3: Website (Recruiter UI)

### 3.1 Test the Website
- [ ] **(b turn)** Go to: `https://01resumemcp.vercel.app/`
- [ ] **(b turn)** Click **"📄 Full Resume"** button
- [ ] **(b turn)** Confirm resume data appears
- [ ] **(b turn)** Click **"💼 Skills"** button
- [ ] **(b turn)** Confirm skills list appears
- [ ] **(b turn)** Click **"⭐ Top Jobs"** button
- [ ] **(b turn)** Confirm job list appears (if you have jobs_raw.csv)
- [ ] **(b turn)** Click **"🎯 Check Job Match"** button
- [ ] **(b turn)** Enter a test job title (e.g., "Software Engineer")
- [ ] **(b turn)** Enter a test job description
- [ ] **(b turn)** Confirm match result appears

### 3.2 Share Website Link
- [ ] **(b turn)** Copy URL: `https://01resumemcp.vercel.app/`
- [ ] **(b turn)** Share with a test recruiter or friend
- [ ] **(b turn)** Ask them to confirm it works

### 3.3 Add Custom Domain (Optional)
- [ ] **(b turn)** Go to Vercel: **Settings** → **Domains**
- [ ] **(b turn)** Click **Add Domain**
- [ ] **(b turn)** Enter: `resume.gozeroshot.dev`
- [ ] **(b turn)** Follow DNS setup instructions
- [ ] **(b turn)** Wait for DNS verification (can take minutes)
- [ ] **(b turn)** Confirm domain shows as "Valid" in Vercel

---

## ✅ Phase 4: ChatGPT Connector

### 4.1 Update/Create ChatGPT Connector
- [ ] **(b turn)** Open ChatGPT (web or desktop)
- [ ] **(b turn)** Go to **Settings** or **Connectors** section
- [ ] **(b turn)** If you have existing "Resume MCP" connector:
  - [ ] **(b turn)** Click **Edit** on "Resume MCP"
- [ ] **(b turn)** If you don't have one:
  - [ ] **(b turn)** Click **Add Connector** or **New Connector**
- [ ] **(b turn)** Set **Name:** `Resume MCP` (or keep existing name)
- [ ] **(b turn)** Set **URL:** `https://01resumemcp.vercel.app/mcp`
- [ ] **(b turn)** Set **Authentication:** Select **"No authentication"**
- [ ] **(b turn)** Click **Save** or **Create**

### 4.2 Test ChatGPT Integration
- [ ] **(b turn)** Start a **new chat** in ChatGPT
- [ ] **(b turn)** Ensure "Resume MCP" connector is enabled/selected for this chat
- [ ] **(b turn)** Ask: "Summarize my resume"
- [ ] **(b turn)** Confirm ChatGPT responds with resume summary
- [ ] **(b turn)** Ask: "What are my top skills?"
- [ ] **(b turn)** Confirm ChatGPT lists your skills
- [ ] **(b turn)** Ask: "Check if I'm a good match for a Senior Software Engineer role"
- [ ] **(b turn)** Confirm ChatGPT uses the MCP tool and provides match analysis

---

## ✅ Phase 5: QR Code for Recruiters

### 5.1 Generate QR Code
- [ ] **(b turn)** Open terminal in project directory
- [ ] **(b turn)** Run: `python3 generate_qr_code.py`
- [ ] **(b turn)** Confirm file `resume_qr_code.png` is created
- [ ] **(b turn)** Open the PNG file to verify QR code looks correct

### 5.2 Use QR Code
- [ ] **(b turn)** Print QR code on business card (optional)
- [ ] **(b turn)** Add QR code to email signature (optional)
- [ ] **(b turn)** Share QR code image digitally with recruiters
- [ ] **(b turn)** Test scanning QR code with phone camera
- [ ] **(b turn)** Confirm it opens the resume website

---

## 🎯 Completion Checklist

- [ ] All Phase 1 steps completed
- [ ] All Phase 2 steps completed (or skipped if not testing)
- [ ] All Phase 3 steps completed
- [ ] All Phase 4 steps completed
- [ ] All Phase 5 steps completed

**Status:** ⬜ Not Started | 🟡 In Progress | ✅ Complete

---

## 📝 Notes

- **API Keys:** Keep OWNER_API_KEY secret, share PUBLIC_API_KEY with trusted users
- **Vercel URL:** `https://01resumemcp.vercel.app/` (may change if you add custom domain)
- **MCP Endpoint:** `https://01resumemcp.vercel.app/mcp`
- **Web UI:** `https://01resumemcp.vercel.app/` (public, no auth needed)

---

**Last Updated:** After authentication setup
**Next Action:** Start with Phase 1, Step 1.1

