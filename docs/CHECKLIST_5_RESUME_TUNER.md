# 📋 Checklist 5: Automated Resume Tuner

**Goal:** Script that rewrites your resume JSON per job cluster. Learn prompt engineering, fine-tuned LLM control, and dynamic resume generation.

**Status:** ⬜ Not Started | 🟡 In Progress | ✅ Complete

**What You'll Learn:**
- Prompt engineering
- LLM fine-tuning (optional)
- Dynamic content generation
- Resume optimization
- A/B testing resumes

---

## 🎯 Phase 0: Understand Resume Tuning

### 0.1 Understand the Concept
- [ ] **(b turn)** Read: Goal = Automatically adjust resume for each job
- [ ] **(b turn)** Read: Different jobs need different emphasis
- [ ] **(b turn)** Read: Tune skills, projects, experience descriptions
- [ ] **(b turn)** Read: Use LLM to rewrite resume sections

### 0.2 Review Current Resume
- [ ] **(b turn)** Open: `resume.json`
- [ ] **(b turn)** Identify: Skills, projects, experience sections
- [ ] **(b turn)** Understand: What can be tuned per job?
- [ ] **(b turn)** Plan: Which sections need dynamic rewriting?

---

## ✅ Phase 1: Job Clustering

### 1.1 Cluster Jobs by Type
- [ ] **(b turn)** Create: `scripts/cluster_jobs.py`
- [ ] **(b turn)** Write script to:
  - Load jobs from `raw/foorila raw.csv`
  - Group by: role type, tech stack, industry
  - Create job clusters (e.g., "ML Engineer", "Data Engineer", "AI Architect")
  - Save to `data/job_clusters.json`
- [ ] **(b turn)** Run: `python scripts/cluster_jobs.py`
- [ ] **(b turn)** Verify: Clusters make sense

### 1.2 Create Cluster Profiles
- [ ] **(b turn)** Create: `data/cluster_profiles.json`
- [ ] **(b turn)** For each cluster, define:
  - Key skills needed
  - Preferred experience
  - Important keywords
  - Tone/style preferences
- [ ] **(b turn)** Example: ML Engineer cluster = emphasize ML, Python, research

---

## ✅ Phase 2: Build Prompt Templates

### 2.1 Create Resume Tuning Prompts
- [ ] **(b turn)** Create: `prompts/resume_tuning_prompts.yaml`
- [ ] **(b turn)** Design prompts for:
  - Skills section tuning
  - Project descriptions tuning
  - Experience descriptions tuning
  - Summary/objective tuning
- [ ] **(b turn)** Example prompt:
  ```yaml
  tune_skills:
    system: "You are a resume optimization expert"
    user: "Given this job: {job_description}, optimize these skills: {current_skills}"
  ```

### 2.2 Test Prompts
- [ ] **(b turn)** Create: `scripts/test_prompts.py`
- [ ] **(b turn)** Write script to:
  - Load prompt templates
  - Test with sample job
  - Generate tuned resume section
  - Print results
- [ ] **(b turn)** Run: `python scripts/test_prompts.py`
- [ ] **(b turn)** Review: Quality of tuned output

---

## ✅ Phase 3: Build Resume Tuner

### 3.1 Create Resume Tuner Script
- [ ] **(b turn)** Create: `resume_tuner/tune_resume.py`
- [ ] **(b turn)** Write code to:
  - Load original `resume.json`
  - Load target job description
  - Identify job cluster
  - Load cluster profile
  - Use LLM to tune each section
  - Generate tuned `resume_tuned.json`
- [ ] **(b turn)** Test: `python resume_tuner/tune_resume.py --job-id 1`
- [ ] **(b turn)** Verify: Tuned resume created

### 3.2 Implement Tuning Strategies
- [ ] **(b turn)** Create: `resume_tuner/strategies.py`
- [ ] **(b turn)** Write strategies:
  - Emphasize relevant skills
  - Rewrite project descriptions
  - Adjust experience focus
  - Optimize keywords
- [ ] **(b turn)** Test: Each strategy individually

---

## ✅ Phase 4: LLM Integration

### 4.1 Set Up OpenAI Client
- [ ] **(b turn)** Create: `resume_tuner/llm_client.py`
- [ ] **(b turn)** Write code to:
  - Initialize OpenAI client
  - Load prompts from YAML
  - Call LLM with prompts
  - Parse responses
- [ ] **(b turn)** Test: LLM calls work

### 4.2 Implement Tuning Functions
- [ ] **(b turn)** Create: `resume_tuner/tuners.py`
- [ ] **(b turn)** Write functions:
  - `tune_skills(resume, job)` - Tune skills section
  - `tune_projects(resume, job)` - Tune projects
  - `tune_experience(resume, job)` - Tune experience
  - `tune_summary(resume, job)` - Tune summary
- [ ] **(b turn)** Test: Each tuning function

---

## ✅ Phase 5: Fine-Tuning (Optional Advanced)

### 5.1 Prepare Fine-Tuning Data
- [ ] **(b turn)** Create: `resume_tuner/finetune_data/`
- [ ] **(b turn)** Create training examples:
  - Original resume section
  - Job description
  - Tuned resume section (target)
- [ ] **(b turn)** Format: JSONL for OpenAI fine-tuning
- [ ] **(b turn)** Create: `scripts/prepare_finetune_data.py`

### 5.2 Fine-Tune Model (If Needed)
- [ ] **(b turn)** Note: Skip if prompt engineering is enough
- [ ] **(b turn)** If doing fine-tuning:
  - Upload training data to OpenAI
  - Create fine-tuning job
  - Wait for completion
  - Use fine-tuned model for tuning

---

## ✅ Phase 6: Resume Comparison

### 6.1 Create Comparison Tool
- [ ] **(b turn)** Create: `resume_tuner/compare.py`
- [ ] **(b turn)** Write code to:
  - Load original resume
  - Load tuned resume
  - Compare sections side-by-side
  - Highlight changes
  - Generate diff report
- [ ] **(b turn)** Test: `python resume_tuner/compare.py original.json tuned.json`

### 6.2 A/B Testing
- [ ] **(b turn)** Create: `resume_tuner/ab_test.py`
- [ ] **(b turn)** Write code to:
  - Generate multiple tuned versions
  - Compare them
  - Score each version
  - Recommend best version
- [ ] **(b turn)** Test: A/B testing workflow

---

## ✅ Phase 7: Integration & API

### 7.1 Add Resume Tuning Endpoint
- [ ] **(b turn)** Open: `server_http.py`
- [ ] **(b turn)** Add: Import resume tuner
- [ ] **(b turn)** Add: Endpoint `POST /api/tune_resume`
  - Takes: job_id or job_description
  - Returns: tuned resume JSON
- [ ] **(b turn)** Test: API endpoint works

### 7.2 Add MCP Tool
- [ ] **(b turn)** Add: New tool `tune_resume_for_job`
- [ ] **(b turn)** Add to `/tools` endpoint
- [ ] **(b turn)** Test: Tool callable via MCP

---

## ✅ Phase 8: Validation & Quality

### 8.1 Validate Tuned Resumes
- [ ] **(b turn)** Create: `resume_tuner/validate.py`
- [ ] **(b turn)** Write validation:
  - Check JSON structure
  - Verify all sections present
  - Check for hallucinations
  - Validate against job requirements
- [ ] **(b turn)** Test: Validation catches errors

### 8.2 Quality Metrics
- [ ] **(b turn)** Create: `resume_tuner/metrics.py`
- [ ] **(b turn)** Compute metrics:
  - Keyword match improvement
  - Skill relevance score
  - Readability score
- [ ] **(b turn)** Test: Metrics computed correctly

---

## 🎯 Success Criteria

- [ ] **(b turn)** Can tune resume for specific job
- [ ] **(b turn)** Tuned resume improves match score
- [ ] **(b turn)** LLM prompts work well
- [ ] **(b turn)** API endpoint works
- [ ] **(b turn)** Can compare original vs. tuned
- [ ] **(b turn)** Quality validation passes

---

## 📝 Notes

**What's Different:**
- Checklist 2: Vector matching (semantic search)
- Checklist 3: ML model (learned patterns)
- Checklist 4: Feature store (structured features)
- Checklist 5: LLM tuning (dynamic content generation)

**Tech Stack:**
- OpenAI API (LLM)
- Prompt engineering
- JSON manipulation
- FastAPI (API)

**Learning Outcomes:**
- ✅ Prompt engineering
- ✅ LLM control
- ✅ Dynamic content generation
- ✅ Resume optimization strategies

---

**Last Updated:** After user request for resume tuner experiment
**Status:** Ready to start Phase 1

