# 📋 Checklist 2: Dynamic Resume with LangChain + Vector Intelligence

**Goal:** Transform Resume MCP into a smart job matching system using LangChain, vector embeddings, and semantic search to get real shortlists of jobs you should apply to.

**Status:** ⬜ Not Started | 🟡 In Progress | ✅ Complete

---

## 🎯 Phase 0: Understand the Vision

### 0.1 Understand the Architecture
- [ ] **(b turn)** Read: Supply side = Resume MCP (your skills)
- [ ] **(b turn)** Read: Demand side = Raw job data (`/raw/foorila raw.csv`)
- [ ] **(b turn)** Read: Goal = Semantic matching using LangChain vectors
- [ ] **(b turn)** Read: Output = Shortlist of jobs ranked by fit score

### 0.2 Review Current State
- [ ] **(b turn)** Check: `resume.json` exists and has skills
- [ ] **(b turn)** Check: `raw/foorila raw.csv` exists with job data
- [ ] **(b turn)** Check: `match_rank.py` has basic matching logic
- [ ] **(b turn)** Understand: Current matching is rule-based, not semantic

---

## ✅ Phase 1: Data Preparation

### 1.1 Normalize Raw Job Data
- [x] ✅ **(b turn)** Opened: `raw/foorila raw.csv` (16 jobs, no description column)
- [x] ✅ **(b turn)** Checked: Columns = company, title, location, salary, URLs (no description)
- [x] ✅ **(b turn)** Created: `scripts/normalize_jobs.py` ✅
- [x] ✅ **(b turn)** Script does:
  - Reads `raw/foorila raw.csv`
  - Creates descriptions from metadata (title + company + location + salary)
  - Standardizes column names
  - Saves to `data/jobs_normalized.csv`
- [x] ✅ **(b turn)** Ran: `python scripts/normalize_jobs.py` ✅
- [x] ✅ **(b turn)** Verified: `data/jobs_normalized.csv` created with 16 jobs + descriptions ✅

### 1.2 Prepare Resume Data
- [x] ✅ **(b turn)** Checked: `resume.json` structure ✅
- [x] ✅ **(b turn)** Verified: Skills are in format: `{"skill_name": weight}` ✅
- [x] ✅ **(b turn)** Created: `langchains/resume_embed_chain.py` (includes text preparation) ✅
- [x] ✅ **(b turn)** Function `create_resume_text()` does:
  - Extracts skills from `resume.json`
  - Creates text representation: "Skills: python(10), sql(9), ml(8)..."
  - Includes projects, experience, etc.
  - Keeps in memory (no file needed)

### 1.3 Create Data Sync Script
- [ ] **(b turn)** Create: `scripts/sync_data.sh` (optional - data already in place)
- [ ] **(b turn)** Write script to:
  - Copy `resume.json` → `data/resume.json` (or use directly)
  - Copy normalized jobs → `data/jobs_normalized.csv` ✅ (already done)
  - Copy `rulebook.yaml` → `data/rulebook.yaml`
- [ ] **(b turn)** Make executable: `chmod +x scripts/sync_data.sh`
- [ ] **(b turn)** Test: `./scripts/sync_data.sh`

**Note:** Data already normalized, can skip this step or create for future updates.

---

## ✅ Phase 2: LangChain Setup

### 2.1 Install Dependencies
- [ ] **(b turn)** Created: `requirements_vector.txt` ✅ (already done)
- [ ] **(b turn)** Install: `pip install -r requirements_vector.txt`
- [ ] **(b turn)** Verify: `python -c "import langchain; print('OK')"`
- [ ] **(b turn)** Verify: `python -c "import chromadb; print('OK')"`
- [ ] **(b turn)** Verify: `python -c "from sentence_transformers import SentenceTransformer; print('OK')"`

**Note:** Using free options first:
- **sentence-transformers** (free, local, no API)
- **Gemini** (free tier)
- **ChromaDB** (free, local)
- OpenAI as fallback only

### 2.2 Set Up Environment
- [ ] **(b turn)** Check: `.env` file exists ✅ (already created)
- [ ] **(b turn)** Verify: API keys added to `.env`:
  - `GEMINI_API_KEY` ✅ (free tier)
  - `GLM_API_KEY` ✅ (free)
  - `FIREWORK_API_KEY` ✅ (cheap)
  - `OPENAI_API_KEY` ✅ (fallback only)
- [ ] **(b turn)** Verify: `.env` is in `.gitignore` ✅
- [ ] **(b turn)** Test: `python -c "from dotenv import load_dotenv; load_dotenv(); import os; print('GEMINI_KEY:', 'SET' if os.getenv('GEMINI_API_KEY') else 'MISSING')"`

### 2.3 Create LangChain Directory Structure
- [x] ✅ **(b turn)** Created: `langchains/` directory ✅
- [x] ✅ **(b turn)** Created: `langchains/__init__.py` ✅
- [x] ✅ **(b turn)** Created: `langchains/resume_embed_chain.py` ✅ (with free embeddings!)
- [ ] **(b turn)** Create: `langchains/job_dna_chain.py`
- [ ] **(b turn)** Create: `langchains/fit_analyzer_chain.py`
- [x] ✅ **(b turn)** Created: `db/` directory for vector stores ✅

---

## ✅ Phase 3: Build Resume Embedding Chain

### 3.1 Create Resume Embed Chain
- [x] ✅ **(b turn)** Opened: `langchains/resume_embed_chain.py` ✅ (already created!)
- [x] ✅ **(b turn)** Code does:
  - Loads resume from `resume.json`
  - Extracts skills, experience, projects
  - Creates text representation
  - Uses **sentence-transformers FIRST** (free, local, no API!)
  - Falls back to Gemini (free tier)
  - OpenAI only if needed
- [ ] **(b turn)** Test: `python langchains/resume_embed_chain.py`
- [ ] **(b turn)** Verify: Embedding works (will save to ChromaDB in next step)

### 3.2 Test Resume Embedding
- [ ] **(b turn)** Create: `test_resume_embed.py`
- [ ] **(b turn)** Write test to:
  - Load resume embedding
  - Query similar skills
  - Print results
- [ ] **(b turn)** Run: `python test_resume_embed.py`
- [ ] **(b turn)** Verify: Can retrieve resume vector successfully

---

## ✅ Phase 4: Build Job DNA Chain

### 4.1 Create Job Embedding Chain
- [ ] **(b turn)** Open: `langchains/job_dna_chain.py`
- [ ] **(b turn)** Write code to:
  - Load jobs from `data/jobs_normalized.csv`
  - For each job, create text: "Title: X, Company: Y, Description: Z"
  - Use OpenAI embeddings to create vectors
  - Store all job vectors in ChromaDB/FAISS
  - Index by job ID
- [ ] **(b turn)** Test: `python langchains/job_dna_chain.py`
- [ ] **(b turn)** Verify: All job vectors stored

### 4.2 Test Job Embedding
- [ ] **(b turn)** Create: `test_job_embed.py`
- [ ] **(b turn)** Write test to:
  - Load job embeddings
  - Query for similar jobs
  - Print top 5 matches
- [ ] **(b turn)** Run: `python test_job_embed.py`
- [ ] **(b turn)** Verify: Can retrieve job vectors successfully

---

## ✅ Phase 5: Build Fit Analyzer Chain

### 5.1 Create Fit Analyzer
- [ ] **(b turn)** Open: `langchains/fit_analyzer_chain.py`
- [ ] **(b turn)** Write code to:
  - Load resume vector
  - Load all job vectors
  - Compute cosine similarity between resume and each job
  - Apply rulebook weights (from `rulebook.yaml`)
  - Combine semantic score + rulebook score
  - Rank jobs by final fit score
- [ ] **(b turn)** Test: `python langchains/fit_analyzer_chain.py`
- [ ] **(b turn)** Verify: Gets ranked list of jobs

### 5.2 Integrate Rulebook Logic
- [ ] **(b turn)** Read: `rulebook.yaml` structure
- [ ] **(b turn)** Modify fit analyzer to:
  - Check positive keywords (boost score)
  - Check negative keywords (reduce score)
  - Apply skill weights
  - Apply match threshold
- [ ] **(b turn)** Test with rulebook: `python langchains/fit_analyzer_chain.py`
- [ ] **(b turn)** Verify: Rulebook affects rankings correctly

### 5.3 Generate Shortlist
- [ ] **(b turn)** Modify fit analyzer to:
  - Filter jobs above match threshold
  - Sort by fit score (descending)
  - Take top N jobs (e.g., top 10)
  - Save to `data/shortlist.csv`
- [ ] **(b turn)** Test: Generate shortlist
- [ ] **(b turn)** Verify: `data/shortlist.csv` created with ranked jobs

---

## ✅ Phase 6: Create API Endpoint

### 6.1 Create Vector Matching API
- [ ] **(b turn)** Create: `api/vector_match.py`
- [ ] **(b turn)** Write FastAPI endpoint:
  - `GET /api/get_shortlist_vector` - Get vector-based shortlist
  - `POST /api/refresh_embeddings` - Re-embed resume and jobs
  - `GET /api/job_fit/{job_id}` - Get fit score for specific job
- [ ] **(b turn)** Integrate with existing `server_http.py`
- [ ] **(b turn)** Test: `curl http://localhost:8000/api/get_shortlist_vector`

### 6.2 Add to MCP Tools
- [ ] **(b turn)** Open: `server_http.py`
- [ ] **(b turn)** Add new tool: `get_vector_shortlist`
- [ ] **(b turn)** Add tool description to `/tools` endpoint
- [ ] **(b turn)** Test: Call tool via MCP endpoint

---

## ✅ Phase 7: Build Dashboard (Optional - Future)

### 7.1 Set Up Next.js (If Building Dashboard)
- [ ] **(b turn)** Create: `app/` directory
- [ ] **(b turn)** Initialize: `npm init next-app app`
- [ ] **(b turn)** Install: Tailwind CSS (optional)
- [ ] **(b turn)** Create: `app/pages/index.js`

### 7.2 Create Dashboard Components
- [ ] **(b turn)** Create: `app/components/JobFitTable.jsx`
- [ ] **(b turn)** Create: `app/components/SkillLegend.jsx`
- [ ] **(b turn)** Create: `app/components/SkillTag.jsx`
- [ ] **(b turn)** Connect to API: Fetch shortlist from backend

### 7.3 Display Results
- [ ] **(b turn)** Show ranked jobs in table
- [ ] **(b turn)** Show fit scores (percentage)
- [ ] **(b turn)** Show skill matches (🟩 matched / ⬜ missing)
- [ ] **(b turn)** Add refresh button to re-run matching

---

## ✅ Phase 8: Testing & Validation

### 8.1 Test with Foorila Data
- [ ] **(b turn)** Ensure: `raw/foorila raw.csv` is normalized
- [ ] **(b turn)** Run: Full pipeline (embed → match → shortlist)
- [ ] **(b turn)** Review: Top 10 jobs in shortlist
- [ ] **(b turn)** Verify: Jobs make sense for your resume
- [ ] **(b turn)** Check: Fit scores are reasonable (0-100%)

### 8.2 Compare with Rule-Based Matching
- [ ] **(b turn)** Run: Old `match_rank.py` (rule-based)
- [ ] **(b turn)** Run: New vector-based matching
- [ ] **(b turn)** Compare: Results from both methods
- [ ] **(b turn)** Analyze: Which jobs appear in both? Which are different?
- [ ] **(b turn)** Document: Differences and why vector matching is better

### 8.3 Test with Himalaya API (Future)
- [ ] **(b turn)** Note: Save for later when ready
- [ ] **(b turn)** Plan: Replace `raw/foorila raw.csv` with Himalaya API
- [ ] **(b turn)** Plan: Create `scripts/fetch_himalaya_jobs.py`

---

## ✅ Phase 9: Documentation & Deployment

### 9.1 Document Vector Matching
- [ ] **(b turn)** Create: `VECTOR_MATCHING_GUIDE.md`
- [ ] **(b turn)** Document: How LangChain vectors work
- [ ] **(b turn)** Document: How semantic matching differs from rule-based
- [ ] **(b turn)** Document: How to refresh embeddings

### 9.2 Update README
- [ ] **(b turn)** Open: `README.md`
- [ ] **(b turn)** Add section: "Vector-Based Job Matching"
- [ ] **(b turn)** Add: How to use new vector shortlist endpoint
- [ ] **(b turn)** Add: Example API calls

### 9.3 Deploy Updated MCP
- [ ] **(b turn)** Test: All endpoints work locally
- [ ] **(b turn)** Push: Code to GitHub
- [ ] **(b turn)** Deploy: To Vercel (if using)
- [ ] **(b turn)** Test: Vector matching works in production

---

## 🐳 Phase 10: Docker (Optional - Explain When Needed)

### 10.1 Understand Docker's Role
- [ ] **(b turn)** Read: Docker explanation below
- [ ] **(b turn)** Decide: Do you need Docker now? (Probably not yet)

**Docker Explanation:**
- **When to use:** When you need consistent environment across machines
- **Why:** Vector stores (ChromaDB/FAISS) need consistent paths
- **Benefit:** Same environment on your Mac, server, cloud
- **Not needed yet:** If only running locally, Docker adds complexity
- **Needed later:** If deploying to cloud or sharing with team

### 10.2 Docker Setup (If Needed Later)
- [ ] **(b turn)** Note: Skip for now, add later if needed
- [ ] **(b turn)** Plan: Dockerfile for vector matching service
- [ ] **(b turn)** Plan: docker-compose.yml for full stack

---

## 🎯 Success Criteria

- [ ] **(b turn)** Can generate shortlist from `raw/foorila raw.csv`
- [ ] **(b turn)** Shortlist is ranked by semantic fit (not just keywords)
- [ ] **(b turn)** Fit scores are explainable (can see why job matches)
- [ ] **(b turn)** Can refresh embeddings when resume updates
- [ ] **(b turn)** API endpoint works: `/api/get_shortlist_vector`
- [ ] **(b turn)** MCP tool works: `get_vector_shortlist`

---

## 📝 Notes

**Current State:**
- ✅ Basic rule-based matching works (`match_rank.py`)
- ✅ Resume data structured (`resume.json`)
- ✅ Raw job data available (`raw/foorila raw.csv`)
- ⬜ Vector embeddings not yet implemented
- ⬜ Semantic matching not yet implemented

**Next Steps:**
1. Start with Phase 1: Normalize job data
2. Then Phase 2: Set up LangChain
3. Then Phase 3-5: Build embedding chains
4. Then Phase 6: Create API
5. Then Phase 7: Build dashboard (optional)

**Key Learning:**
- LangChain vectors = Convert text to numbers (embeddings)
- Semantic search = Find similar meaning, not just keywords
- Vector matching = Compare resume vector with job vectors
- Fit score = Combination of semantic similarity + rulebook logic

---

**Last Updated:** After user request for vector-based matching
**Status:** Ready to start Phase 1

