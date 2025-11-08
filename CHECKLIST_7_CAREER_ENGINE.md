# 📋 Checklist 7: Career Recommendation Engine

**Goal:** Use embeddings (FAISS/Chroma) on your job and skill data. Learn vector search, similarity models, retrieval pipelines, and career path recommendations.

**Status:** ⬜ Not Started | 🟡 In Progress | ✅ Complete

**What You'll Learn:**
- Vector search (FAISS/Chroma)
- Similarity models
- Retrieval pipelines
- Career path recommendations
- Embedding strategies

---

## 🎯 Phase 0: Understand Vector Search

### 0.1 Understand Vector Search
- [ ] **(b turn)** Read: Vector search = Find similar items using embeddings
- [ ] **(b turn)** Read: Embeddings = Text converted to numbers (vectors)
- [ ] **(b turn)** Read: Similarity = Distance between vectors
- [ ] **(b turn)** Read: FAISS = Fast vector search library
- [ ] **(b turn)** Read: Chroma = Vector database

### 0.2 Review What's Already Done
- [ ] **(b turn)** Check: Checklist 2 has LangChain embeddings (can reuse)
- [ ] **(b turn)** Check: `resume.json` exists
- [ ] **(b turn)** Check: `raw/foorila raw.csv` exists
- [ ] **(b turn)** Understand: This builds on Checklist 2 but focuses on recommendations

---

## ✅ Phase 1: Set Up Vector Store

### 1.1 Choose Vector Store
- [ ] **(b turn)** Decide: FAISS (fast, local) or Chroma (persistent, queryable)
- [ ] **(b turn)** Read: FAISS = Better for large-scale, in-memory
- [ ] **(b turn)** Read: Chroma = Better for persistence, metadata filtering
- [ ] **(b turn)** Choose: Start with Chroma (easier), can add FAISS later

### 1.2 Install Dependencies
- [ ] **(b turn)** Create: `requirements_vector.txt`
- [ ] **(b turn)** Add:
  - chromadb>=0.4.0
  - faiss-cpu>=1.7.4 (optional)
  - langchain>=0.1.0
  - langchain-community>=0.0.20
  - openai>=1.0.0
- [ ] **(b turn)** Install: `pip install -r requirements_vector.txt`
- [ ] **(b turn)** Verify: Can import chromadb

---

## ✅ Phase 2: Embed Resume & Skills

### 2.1 Create Resume Embeddings
- [ ] **(b turn)** Create: `career_engine/embed_resume.py`
- [ ] **(b turn)** Write code to:
  - Load `resume.json`
  - Extract: Skills, experience, projects
  - Create text representation
  - Generate embeddings (OpenAI or sentence-transformers)
  - Store in ChromaDB collection: "resume"
- [ ] **(b turn)** Test: `python career_engine/embed_resume.py`
- [ ] **(b turn)** Verify: Embeddings stored in ChromaDB

### 2.2 Create Skill Embeddings
- [ ] **(b turn)** Create: `career_engine/embed_skills.py`
- [ ] **(b turn)** Write code to:
  - Extract all skills from resume
  - Embed each skill individually
  - Store in ChromaDB collection: "skills"
  - Add metadata: skill name, weight, category
- [ ] **(b turn)** Test: `python career_engine/embed_skills.py`
- [ ] **(b turn)** Verify: Skill embeddings stored

---

## ✅ Phase 3: Embed Jobs

### 3.1 Create Job Embeddings
- [ ] **(b turn)** Create: `career_engine/embed_jobs.py`
- [ ] **(b turn)** Write code to:
  - Load jobs from `raw/foorila raw.csv`
  - For each job, create text: "Title: X, Company: Y, Description: Z"
  - Generate embeddings
  - Store in ChromaDB collection: "jobs"
  - Add metadata: company, title, location, salary
- [ ] **(b turn)** Test: `python career_engine/embed_jobs.py`
- [ ] **(b turn)** Verify: All job embeddings stored

### 3.2 Index Jobs for Fast Search
- [ ] **(b turn)** Create: `career_engine/index_jobs.py`
- [ ] **(b turn)** Write code to:
  - Load job embeddings
  - Create FAISS index (optional, for speed)
  - Or optimize ChromaDB index
- [ ] **(b turn)** Test: Index created successfully

---

## ✅ Phase 4: Build Similarity Search

### 4.1 Create Job Similarity Search
- [ ] **(b turn)** Create: `career_engine/find_similar_jobs.py`
- [ ] **(b turn)** Write code to:
  - Load resume embedding
  - Query ChromaDB for similar jobs
  - Return top N most similar jobs
  - Include similarity scores
- [ ] **(b turn)** Test: `python career_engine/find_similar_jobs.py`
- [ ] **(b turn)** Verify: Returns relevant jobs

### 4.2 Create Skill-Based Search
- [ ] **(b turn)** Create: `career_engine/find_jobs_by_skill.py`
- [ ] **(b turn)** Write code to:
  - Take a skill name
  - Find similar skills in vector space
  - Find jobs that match those skills
  - Return ranked list
- [ ] **(b turn)** Test: Skill-based search works

---

## ✅ Phase 5: Build Career Recommendations

### 5.1 Create Career Path Analyzer
- [ ] **(b turn)** Create: `career_engine/career_paths.py`
- [ ] **(b turn)** Write code to:
  - Analyze your current skills
  - Find similar career paths in job data
  - Identify skill gaps
  - Recommend next skills to learn
- [ ] **(b turn)** Test: Career path analysis works

### 5.2 Create Skill Gap Analysis
- [ ] **(b turn)** Create: `career_engine/skill_gaps.py`
- [ ] **(b turn)** Write code to:
  - Compare your skills vs. target job
  - Identify missing skills
  - Rank missing skills by importance
  - Suggest learning path
- [ ] **(b turn)** Test: Skill gap analysis works

---

## ✅ Phase 6: Build Recommendation Engine

### 6.1 Create Recommendation Pipeline
- [ ] **(b turn)** Create: `career_engine/recommend.py`
- [ ] **(b turn)** Write code to:
  - Combine multiple signals:
    - Job similarity (vector search)
    - Skill match (rule-based)
    - Career path fit
    - Skill gap analysis
  - Generate final recommendation score
  - Rank jobs by recommendation score
- [ ] **(b turn)** Test: `python career_engine/recommend.py`
- [ ] **(b turn)** Verify: Recommendations make sense

### 6.2 Add Explainability
- [ ] **(b turn)** Create: `career_engine/explain_recommendation.py`
- [ ] **(b turn)** Write code to:
  - For each recommendation, explain why
  - Show: Similar skills, career path match, gap analysis
  - Generate human-readable explanation
- [ ] **(b turn)** Test: Explanations are clear

---

## ✅ Phase 7: Build API Endpoints

### 7.1 Create Recommendation API
- [ ] **(b turn)** Create: `career_engine/api.py`
- [ ] **(b turn)** Write FastAPI endpoints:
  - `GET /recommendations` - Get top job recommendations
  - `GET /recommendations/{job_id}` - Get recommendation for specific job
  - `GET /career_paths` - Get career path suggestions
  - `GET /skill_gaps/{job_id}` - Get skill gaps for job
  - `POST /similar_jobs` - Find similar jobs to given job
- [ ] **(b turn)** Test: All endpoints work

### 7.2 Integrate with Resume MCP
- [ ] **(b turn)** Open: `server_http.py`
- [ ] **(b turn)** Add: Import career engine
- [ ] **(b turn)** Add: New MCP tools:
  - `get_career_recommendations`
  - `get_similar_jobs`
  - `analyze_skill_gaps`
  - `get_career_paths`
- [ ] **(b turn)** Test: Tools callable via MCP

---

## ✅ Phase 8: Advanced Features

### 8.1 Add Career Progression Tracking
- [ ] **(b turn)** Create: `career_engine/track_progress.py`
- [ ] **(b turn)** Write code to:
  - Track skill development over time
  - Compare current vs. past resume
  - Show progress toward career goals
- [ ] **(b turn)** Test: Progress tracking works

### 8.2 Add Multi-Model Comparison
- [ ] **(b turn)** Create: `career_engine/compare_models.py`
- [ ] **(b turn)** Write code to:
  - Compare FAISS vs. ChromaDB results
  - Compare different embedding models
  - Show which performs better
- [ ] **(b turn)** Test: Model comparison works

---

## ✅ Phase 9: Optimization

### 9.1 Optimize Vector Search
- [ ] **(b turn)** Research: FAISS index types (IVF, HNSW)
- [ ] **(b turn)** Implement: Faster index if using FAISS
- [ ] **(b turn)** Test: Search speed improved

### 9.2 Add Caching
- [ ] **(b turn)** Create: `career_engine/cache.py`
- [ ] **(b turn)** Implement:
  - Cache embeddings
  - Cache search results
  - Cache recommendations
- [ ] **(b turn)** Test: Caching improves performance

---

## 🎯 Success Criteria

- [ ] **(b turn)** Resume and jobs embedded in vector store
- [ ] **(b turn)** Can find similar jobs using vector search
- [ ] **(b turn)** Career recommendations generated
- [ ] **(b turn)** Skill gap analysis works
- [ ] **(b turn)** API endpoints work
- [ ] **(b turn)** Integrated with Resume MCP

---

## 📝 Notes

**What's Different:**
- Checklist 2: LangChain embeddings (semantic search)
- Checklist 7: Vector search + career recommendations (this one)

**Tech Stack:**
- ChromaDB or FAISS (vector stores)
- OpenAI embeddings (or sentence-transformers)
- LangChain (optional, for chains)
- FastAPI (API)

**Learning Outcomes:**
- ✅ Vector search
- ✅ Similarity models
- ✅ Retrieval pipelines
- ✅ Career path analysis

---

**Last Updated:** After user request for career engine experiment
**Status:** Ready to start Phase 1

