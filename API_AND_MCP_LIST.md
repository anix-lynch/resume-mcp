# 📋 Current API & MCP Tools List

**Last Updated:** After Checklist 2 creation
**Status:** Ready to start LangChain vector implementation

---

## 🔌 Current MCP Tools (14 Tools)

### Resume MCP Tools (Tech Resume)
1. **`get_resume_info`** - Get full tech resume information
2. **`get_skills`** - Get skills with weights
3. **`get_shortlist`** - Get top job matches (rule-based)
4. **`check_job_match`** - Check if a specific job matches

### B Past Life MCP Tools (VC/PE/Finance Resume)
5. **`get_b_past_life_resume_info`** - Get past life resume
6. **`check_b_past_life_job_match`** - Check job match for past life resume

### Northstar MCP Tools (Project Registry)
7. **`get_northstar_info`** - Get Northstar suite overview
8. **`list_projects`** - List all 5 projects
9. **`get_project`** - Get project by ID (1-5)
10. **`get_project_by_name`** - Get project by name
11. **`get_shared_assets`** - Get shared assets
12. **`get_ai_agent_plan`** - Get AI orchestration plan
13. **`search_projects`** - Search projects by keyword

### Combined Tools
14. **`get_all_resumes`** - Get all resume types (tech + past life)

---

## 🌐 Current API Endpoints

### Public Endpoints (No Auth)
- **`GET /`** - Web UI (recruiter interface)

### Protected Endpoints (Auth Required)
- **`GET/POST /mcp`** - MCP protocol endpoint
- **`GET /tools`** - List all MCP tools
- **`POST /call`** - Call an MCP tool
- **`GET /api/get_resume_info`** - Get full resume
- **`GET /api/get_skills`** - Get skills
- **`GET /api/get_shortlist`** - Get job shortlist
- **`POST /api/check_job_match`** - Check job match

---

## 📊 Current Data Files

### Supply Side (Resume)
- ✅ `resume.json` - Tech resume
- ✅ `b_past_life_mcp/resume.json` - Past life resume
- ✅ `rulebook.yaml` - Matching rules

### Demand Side (Jobs)
- ✅ `raw/foorila raw.csv` - Real job data (17 jobs)
- ✅ `raw/jobs_raw.csv` - Additional jobs
- ✅ `raw/linkedin_jobs.csv` - LinkedIn jobs
- ✅ `raw/builtinla_jobs.csv` - Built In LA jobs
- ✅ `raw/airtable_random.csv` - Airtable jobs

### Generated Files
- ⬜ `jobs_clean.csv` - Cleaned jobs (generated)
- ⬜ `shortlist.csv` - Top matches (generated)
- ⬜ `discard.csv` - Filtered out jobs (generated)

---

## 🎯 What You Need to Start Checklist 2

### Phase 1: Data Preparation
**What you need:**
- ✅ `resume.json` - Already have
- ✅ `raw/foorila raw.csv` - Already have (17 jobs)
- ⬜ Normalized job data - Need to create

**What I need from you:**
- [ ] **(b turn)** Confirm: `raw/foorila raw.csv` is the main job source
- [ ] **(b turn)** Check: Does it have job descriptions? (or just title/company?)
- [ ] **(b turn)** Decide: Use all 17 jobs or filter some?

### Phase 2: LangChain Setup
**What you need:**
- ⬜ OpenAI API key - Need to set
- ⬜ LangChain installed - Need to install
- ⬜ Vector store (ChromaDB/FAISS) - Need to set up

**What I need from you:**
- [ ] **(b turn)** Do you have OpenAI API key? (Yes/No)
- [ ] **(b turn)** If yes, add to `.env` file
- [ ] **(b turn)** If no, get one from: https://platform.openai.com/api-keys

### Phase 3-5: Building Chains
**What you need:**
- ⬜ Resume embedding chain - Need to build
- ⬜ Job embedding chain - Need to build
- ⬜ Fit analyzer chain - Need to build

**What I need from you:**
- [ ] **(b turn)** Start with Phase 1, Step 1.1
- [ ] **(b turn)** I'll guide you through each step

---

## 🚀 Quick Start Checklist 2

### Step 1: Check Your Data
- [ ] **(b turn)** Open: `raw/foorila raw.csv`
- [ ] **(b turn)** Check: What columns does it have?
- [ ] **(b turn)** Note: Does it have job descriptions or just metadata?

### Step 2: Set Up Environment
- [ ] **(b turn)** Check: Do you have OpenAI API key?
- [ ] **(b turn)** If yes: Add to `.env` file
- [ ] **(b turn)** If no: Get one first

### Step 3: Install Dependencies
- [ ] **(b turn)** I'll create `requirements_vector.txt`
- [ ] **(b turn)** You run: `pip install -r requirements_vector.txt`

### Step 4: Start Phase 1
- [ ] **(b turn)** Open: `CHECKLIST_2_LANGCHAIN_VECTOR.md`
- [ ] **(b turn)** Start with Phase 1, Step 1.1
- [ ] **(b turn)** I'll help you through each step

---

## 💡 What I Can Do Right Now

**I can:**
- ✅ Check your current API/MCP setup
- ✅ Create normalization script for jobs
- ✅ Set up LangChain structure
- ✅ Guide you step-by-step

**I need from you:**
- ⬜ Confirm job data structure (what columns in foorila CSV?)
- ⬜ OpenAI API key (or confirm you have one)
- ⬜ Start Phase 1 when ready

---

**Ready to start?** Tell me:
1. Do you have OpenAI API key?
2. What columns are in `raw/foorila raw.csv`? (I can check if you want)
3. Ready to start Phase 1?

