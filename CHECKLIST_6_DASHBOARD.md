# 📋 Checklist 6: Job Match Dashboard

**Goal:** Streamlit or Gradio container visualizing which jobs fit best. Learn data visualization, containerized web apps, and interactive dashboards.

**Status:** ⬜ Not Started | 🟡 In Progress | ✅ Complete

**What You'll Learn:**
- Streamlit or Gradio
- Data visualization
- Containerized web apps
- Interactive dashboards
- Real-time updates

---

## 🎯 Phase 0: Choose Dashboard Framework

### 0.1 Decide on Framework
- [ ] **(b turn)** Research: Streamlit vs. Gradio
- [ ] **(b turn)** Read: Streamlit = Python-first, easy
- [ ] **(b turn)** Read: Gradio = More customizable, ML-focused
- [ ] **(b turn)** Choose: Streamlit (recommended for simplicity) or Gradio
- [ ] **(b turn)** Note: Can switch later if needed

### 0.2 Understand Dashboard Goals
- [ ] **(b turn)** Read: Show job rankings
- [ ] **(b turn)** Read: Show skill matches (🟩/⬜)
- [ ] **(b turn)** Read: Show fit scores
- [ ] **(b turn)** Read: Allow filtering and sorting

---

## ✅ Phase 1: Set Up Dashboard Project

### 1.1 Create Dashboard Directory
- [ ] **(b turn)** Create: `dashboard/` directory
- [ ] **(b turn)** Create: `dashboard/app.py` (Streamlit) or `dashboard/app.py` (Gradio)
- [ ] **(b turn)** Create: `dashboard/requirements.txt`
- [ ] **(b turn)** Add dependencies:
  - streamlit (or gradio)
  - pandas
  - plotly (for charts)
  - requests (to call Resume MCP API)

### 1.2 Install Dependencies
- [ ] **(b turn)** Install: `pip install -r dashboard/requirements.txt`
- [ ] **(b turn)** Test: `streamlit --version` (or `gradio --version`)
- [ ] **(b turn)** Verify: Can import libraries

---

## ✅ Phase 2: Build Basic Dashboard

### 2.1 Create Main Dashboard Layout
- [ ] **(b turn)** Open: `dashboard/app.py`
- [ ] **(b turn)** Write Streamlit app (or Gradio):
  - Title: "Job Match Dashboard"
  - Sidebar: Filters and controls
  - Main area: Job table
  - Footer: Last updated time
- [ ] **(b turn)** Test: `streamlit run dashboard/app.py`
- [ ] **(b turn)** Verify: Dashboard loads in browser

### 2.2 Connect to Resume MCP API
- [ ] **(b turn)** Create: `dashboard/api_client.py`
- [ ] **(b turn)** Write code to:
  - Call Resume MCP API: `/api/get_shortlist`
  - Call: `/api/get_resume_info`
  - Handle errors
  - Cache results
- [ ] **(b turn)** Test: Can fetch data from API

---

## ✅ Phase 3: Display Job Rankings

### 3.1 Create Job Table Component
- [ ] **(b turn)** Create: `dashboard/components/job_table.py`
- [ ] **(b turn)** Write component to:
  - Display jobs in table
  - Show: Rank, Company, Title, Fit Score
  - Make sortable
  - Add clickable links
- [ ] **(b turn)** Test: Table displays correctly

### 3.2 Add Skill Match Visualization
- [ ] **(b turn)** Create: `dashboard/components/skill_tags.py`
- [ ] **(b turn)** Write component to:
  - Show skills as tags
  - Color code: 🟩 matched, ⬜ missing
  - Add tooltips with details
- [ ] **(b turn)** Test: Skill tags display correctly

---

## ✅ Phase 4: Add Visualizations

### 4.1 Create Fit Score Chart
- [ ] **(b turn)** Create: `dashboard/components/fit_chart.py`
- [ ] **(b turn)** Write code to:
  - Create bar chart of fit scores
  - Use Plotly or Streamlit charts
  - Show top 10 jobs
- [ ] **(b turn)** Test: Chart displays

### 4.2 Create Skill Distribution Chart
- [ ] **(b turn)** Create: `dashboard/components/skill_chart.py`
- [ ] **(b turn)** Write code to:
  - Show which skills are most matched
  - Create pie chart or bar chart
  - Show skill frequency across jobs
- [ ] **(b turn)** Test: Chart displays

---

## ✅ Phase 5: Add Interactivity

### 5.1 Add Filters
- [ ] **(b turn)** Add to sidebar:
  - Filter by company
  - Filter by fit score range
  - Filter by location
  - Filter by remote
- [ ] **(b turn)** Test: Filters work

### 5.2 Add Job Details View
- [ ] **(b turn)** Create: `dashboard/components/job_detail.py`
- [ ] **(b turn)** Write component to:
  - Show full job details when clicked
  - Show match breakdown
  - Show why job matches/doesn't match
- [ ] **(b turn)** Test: Details view works

---

## ✅ Phase 6: Dockerize Dashboard

### 6.1 Create Dockerfile
- [ ] **(b turn)** Create: `dashboard/Dockerfile`
- [ ] **(b turn)** Write Dockerfile:
  ```dockerfile
  FROM python:3.11-slim
  WORKDIR /app
  COPY requirements.txt .
  RUN pip install -r requirements.txt
  COPY . .
  EXPOSE 8501
  CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
  ```

### 6.2 Build and Run Container
- [ ] **(b turn)** Build: `docker build -t resume-dashboard ./dashboard/`
- [ ] **(b turn)** Run: `docker run -p 8501:8501 resume-dashboard`
- [ ] **(b turn)** Test: Dashboard accessible at http://localhost:8501

---

## ✅ Phase 7: Real-Time Updates

### 7.1 Add Refresh Button
- [ ] **(b turn)** Add: Refresh button to dashboard
- [ ] **(b turn)** On click: Re-fetch data from API
- [ ] **(b turn)** Show: Loading indicator
- [ ] **(b turn)** Test: Refresh works

### 7.2 Add Auto-Refresh (Optional)
- [ ] **(b turn)** Add: Auto-refresh every N minutes
- [ ] **(b turn)** Use: Streamlit's auto-refresh or polling
- [ ] **(b turn)** Test: Auto-refresh works

---

## ✅ Phase 8: Advanced Features

### 8.1 Add Export Functionality
- [ ] **(b turn)** Add: Export shortlist to CSV
- [ ] **(b turn)** Add: Export to PDF (optional)
- [ ] **(b turn)** Test: Export works

### 8.2 Add Comparison View
- [ ] **(b turn)** Create: `dashboard/components/compare_jobs.py`
- [ ] **(b turn)** Write component to:
  - Compare 2-3 jobs side-by-side
  - Show differences
  - Highlight best match
- [ ] **(b turn)** Test: Comparison view works

---

## ✅ Phase 9: Deployment

### 9.1 Deploy to Streamlit Cloud (If Using Streamlit)
- [ ] **(b turn)** Push: Dashboard code to GitHub
- [ ] **(b turn)** Go to: streamlit.io
- [ ] **(b turn)** Deploy: Connect GitHub repo
- [ ] **(b turn)** Configure: Environment variables (API URL)
- [ ] **(b turn)** Test: Deployed dashboard works

### 9.2 Deploy to Vercel (Alternative)
- [ ] **(b turn)** Create: `dashboard/vercel.json`
- [ ] **(b turn)** Configure: For Streamlit or Gradio
- [ ] **(b turn)** Deploy: `vercel --prod`
- [ ] **(b turn)** Test: Deployed dashboard works

---

## 🎯 Success Criteria

- [ ] **(b turn)** Dashboard displays job rankings
- [ ] **(b turn)** Shows skill matches (🟩/⬜)
- [ ] **(b turn)** Shows fit scores
- [ ] **(b turn)** Filters work
- [ ] **(b turn)** Charts display correctly
- [ ] **(b turn)** Runs in Docker container
- [ ] **(b turn)** Deployed and accessible

---

## 📝 Notes

**Framework Choice:**
- **Streamlit:** Easier, Python-first, good for data apps
- **Gradio:** More customizable, better for ML demos

**Tech Stack:**
- Streamlit or Gradio
- Plotly (charts)
- Docker (containerization)
- FastAPI (backend API)

**Learning Outcomes:**
- ✅ Data visualization
- ✅ Interactive dashboards
- ✅ Containerized web apps
- ✅ Real-time data updates

---

**Last Updated:** After user request for dashboard experiment
**Status:** Ready to start Phase 1

