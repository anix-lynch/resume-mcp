# Resume MCP – Job Recommender

**Northstar Project #1** | ZeroShot Brand

A minimal, CLI-first data-engineering pipeline that ingests job data, filters it with a rulebook, ranks each job against resume facts, and outputs a shortlist ready for manual application.

## 🎯 Goal

Build the brain of a two-sided marketplace (Me ↔ Job Market) that:
- Ingests raw job postings
- Cleans and deduplicates data
- Filters using positive/negative keyword rules
- Ranks jobs against resume skills and experience
- Outputs top-5 shortlist + discarded jobs

## 📊 Workflow

```
jobs_raw.csv
    │
    ├─→ etl_clean.py
    │       │
    │       └─→ jobs_clean.csv
    │
    ├─→ rulebook.yaml (filter rules)
    │
    ├─→ resume.json (skills, projects, weights)
    │
    └─→ match_rank.py
            │
            ├─→ shortlist.csv (top 5)
            └─→ discard.csv (filtered out)
```

## 🚀 Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Set up environment (optional)
cp .env.example .env
# Edit .env with your API_URL and DB_PATH

# 3. Run the pipeline
python etl_clean.py
python match_rank.py

# 4. Preview top matches
python match_rank.py --preview

# 5. Sync to API (optional)
./sync_to_api.sh
```

## 📁 Project Structure

```
01_resume_mcp/
├── README.md              # This file
├── jobs_raw.csv           # Sample 10-row raw input
├── jobs_clean.csv         # Normalized output (generated)
├── shortlist.csv          # Top-5 ranked jobs (generated)
├── discard.csv            # Filtered-out jobs (generated)
├── resume.json            # Resume facts (skills, projects, weights)
├── rulebook.yaml          # Positive/negative keyword rules
├── match_rank.py          # Core ranking logic
├── etl_clean.py           # Basic dedupe + cleanup
├── sync_to_api.sh         # Posts clean data to shared API
├── requirements.txt       # Dependencies
└── .env.example           # API_URL and DB_PATH placeholders
```

## 🔧 Components

### `etl_clean.py`
- Deduplicates job postings by URL
- Normalizes company names and titles
- Cleans whitespace and formatting
- Outputs `jobs_clean.csv`

### `match_rank.py`
- Loads `resume.json` and `rulebook.yaml`
- Filters jobs using positive/negative keywords
- Scores each job using keyword overlap + text similarity
- Ranks and outputs top-5 to `shortlist.csv`
- Moves filtered jobs to `discard.csv`

### `rulebook.yaml`
- Positive keywords: must-have terms (e.g., "Python", "ML", "Data Engineering")
- Negative keywords: deal-breakers (e.g., "internship", "junior only")

### `resume.json`
- Skills with weights (importance scores)
- Projects with tech stack
- Experience highlights
- Used for matching and ranking

## 📝 Input Format

`jobs_raw.csv` columns:
- `title`: Job title
- `company`: Company name
- `url`: Job posting URL
- `source`: Where the job was found (optional)

## 📤 Output Format

### `shortlist.csv`
Top 5 ranked jobs with:
- All original columns
- `match_score`: 0-100 ranking score
- `matched_skills`: List of matched skills
- `matched_projects`: List of matched projects

### `discard.csv`
Jobs filtered out due to:
- Negative keyword matches
- Low match scores
- Missing required positive keywords

## 🎨 Preview Mode

```bash
python match_rank.py --preview
```

Prints a pretty table of top-5 matches with:
- Job title and company
- Match score
- Key matched skills
- Match reason

## 🔄 API Sync (Optional)

```bash
./sync_to_api.sh
```

Posts `jobs_clean.csv` and `shortlist.csv` to a shared FastAPI endpoint:
- `POST /resume/jobs` → clean jobs
- `POST /resume/shortlist` → top matches

Requires `API_URL` in `.env`.

## 🛠️ Design Principles

- **CLI-first**: No GUI, no notebooks
- **Deterministic**: No LLM calls, pure data processing
- **Lightweight**: Standard Python + pandas (DuckDB optional)
- **Local-first**: Runs entirely on your machine
- **Clear logging**: Error handling and sanity checks included

## 📋 Requirements

- Python 3.8+
- pandas
- pyyaml
- requests (for API sync)
- duckdb (optional, for advanced queries)

## 🤖 OpenAI SDK Integration

Your MCP is ready! You can now use OpenAI SDK to interact with your resume matching system.

### Option 1: OpenAI Agents MCP (Recommended)

```bash
# Set your API key
export OPENAI_API_KEY='your-key-here'

# Run the interactive chat
python talk_to_app.py agents
```

This uses the `openai-agents-mcp` package to connect OpenAI Agents SDK with your MCP server.

### Option 2: FastAPI REST API

```bash
# Start the API server
python api_server.py

# In another terminal, use OpenAI SDK with function calling
python talk_to_app.py direct
```

The API server exposes endpoints that OpenAI SDK can call:
- `GET /resume` - Get resume info
- `GET /resume/skills` - Get skills
- `POST /jobs/match` - Match jobs
- `GET /jobs/shortlist` - Get top matches
- `POST /jobs/check` - Check specific job match

### Option 3: Direct MCP Server

```bash
# Run MCP server (stdio mode)
python server.py
```

Then connect via MCP client or use with Cursor/Claude Code.

### Files Added

- `server.py` - MCP protocol server with tools
- `api_server.py` - FastAPI REST API (alternative)
- `talk_to_app.py` - OpenAI SDK integration examples
- `mcp_agent_config.yaml` - MCP server configuration

## 🔗 Future Integration

This project will feed into **Project #4 – Dynamic Resume**, which will visualize:
- Current top skills and projects
- Most compatible jobs
- Real-time updates from this pipeline

---

**Status**: Ready to run | MCP-enabled | OpenAI SDK compatible

