# 📋 Checklist 3: Docker-ized ML Filter

**Goal:** Train a small ML model inside Docker that scores job posts vs. your resume JSON. Learn model serving, reproducibility, and data pipelines.

**Status:** ⬜ Not Started | 🟡 In Progress | ✅ Complete

**What You'll Learn:**
- Docker containerization
- ML model training (scikit-learn)
- Model serving (FastAPI in Docker)
- Reproducible ML pipelines
- Data versioning

---

## 🎯 Phase 0: Understand the Goal

### 0.1 Understand ML Filter Concept
- [ ] **(b turn)** Read: Goal is to train a model that scores jobs (0-100) based on resume match
- [ ] **(b turn)** Read: Model will be trained on features from resume.json + job descriptions
- [ ] **(b turn)** Read: Model runs in Docker for reproducibility
- [ ] **(b turn)** Read: Model serves predictions via API endpoint

### 0.2 Review What's Already Done
- [ ] **(b turn)** Check: `resume.json` exists (supply side)
- [ ] **(b turn)** Check: `raw/foorila raw.csv` exists (demand side)
- [ ] **(b turn)** Check: `match_rank.py` has basic scoring (use as baseline)
- [ ] **(b turn)** Understand: Current matching is rule-based, ML will learn patterns

---

## ✅ Phase 1: Prepare Training Data

### 1.1 Create Labeled Dataset
- [ ] **(b turn)** Create: `ml_data/` directory
- [ ] **(b turn)** Create: `scripts/create_training_data.py`
- [ ] **(b turn)** Write script to:
  - Load `resume.json` and `raw/foorila raw.csv`
  - For each job, compute features:
    - Skill overlap count
    - Keyword match score
    - Experience level match
    - Salary range match (if available)
    - Location match (remote preference)
  - Create labels: Use `match_rank.py` scores as ground truth (or manually label)
  - Save to `ml_data/training_data.csv`
- [ ] **(b turn)** Run: `python scripts/create_training_data.py`
- [ ] **(b turn)** Verify: `ml_data/training_data.csv` has features + labels

### 1.2 Split Training/Test Data
- [ ] **(b turn)** Create: `scripts/split_data.py`
- [ ] **(b turn)** Write script to:
  - Load `ml_data/training_data.csv`
  - Split 80/20 (train/test)
  - Save to `ml_data/train.csv` and `ml_data/test.csv`
- [ ] **(b turn)** Run: `python scripts/split_data.py`
- [ ] **(b turn)** Verify: Both files created

---

## ✅ Phase 2: Build ML Model

### 2.1 Create Model Training Script
- [ ] **(b turn)** Create: `ml/train_model.py`
- [ ] **(b turn)** Write code to:
  - Load training data
  - Feature engineering (normalize, encode)
  - Train model (start with RandomForest or XGBoost)
  - Evaluate on test set
  - Save model to `ml/models/job_match_model.pkl`
- [ ] **(b turn)** Test: `python ml/train_model.py`
- [ ] **(b turn)** Verify: Model file created, accuracy > baseline

### 2.2 Evaluate Model
- [ ] **(b turn)** Create: `ml/evaluate_model.py`
- [ ] **(b turn)** Write code to:
  - Load saved model
  - Load test data
  - Compute metrics: accuracy, precision, recall, F1
  - Print confusion matrix
  - Save evaluation report
- [ ] **(b turn)** Run: `python ml/evaluate_model.py`
- [ ] **(b turn)** Review: Model performance metrics

---

## ✅ Phase 3: Dockerize Model

### 3.1 Create Dockerfile for ML Service
- [ ] **(b turn)** Create: `ml/Dockerfile`
- [ ] **(b turn)** Write Dockerfile:
  ```dockerfile
  FROM python:3.11-slim
  WORKDIR /app
  COPY requirements_ml.txt .
  RUN pip install -r requirements_ml.txt
  COPY ml/ ./ml/
  COPY ml_data/ ./ml_data/
  CMD ["python", "ml/serve_model.py"]
  ```
- [ ] **(b turn)** Create: `ml/requirements_ml.txt` with:
  - scikit-learn
  - pandas
  - fastapi
  - uvicorn
  - joblib (for model loading)

### 3.2 Create Model Serving API
- [ ] **(b turn)** Create: `ml/serve_model.py`
- [ ] **(b turn)** Write FastAPI app to:
  - Load model on startup
  - Endpoint: `POST /predict` - Takes job data, returns score
  - Endpoint: `GET /health` - Health check
  - Endpoint: `GET /model_info` - Model metadata
- [ ] **(b turn)** Test locally: `python ml/serve_model.py`
- [ ] **(b turn)** Test: `curl -X POST http://localhost:8001/predict -d '{"job": {...}}'`

### 3.3 Build Docker Image
- [ ] **(b turn)** Build: `docker build -t resume-ml-filter ./ml/`
- [ ] **(b turn)** Verify: `docker images | grep resume-ml-filter`
- [ ] **(b turn)** Run: `docker run -p 8001:8001 resume-ml-filter`
- [ ] **(b turn)** Test: API works in container

---

## ✅ Phase 4: Integrate with Resume MCP

### 4.1 Add ML Prediction Endpoint
- [ ] **(b turn)** Open: `server_http.py`
- [ ] **(b turn)** Add: Import requests library
- [ ] **(b turn)** Add: Function to call ML service
- [ ] **(b turn)** Add: New MCP tool: `get_ml_job_score`
- [ ] **(b turn)** Add tool to `/tools` endpoint
- [ ] **(b turn)** Test: Call tool via MCP

### 4.2 Create Docker Compose
- [ ] **(b turn)** Create: `docker-compose.ml.yml`
- [ ] **(b turn)** Write compose file:
  - Service: `resume-mcp` (existing)
  - Service: `ml-filter` (new ML service)
  - Network: Connect both services
- [ ] **(b turn)** Test: `docker-compose -f docker-compose.ml.yml up`
- [ ] **(b turn)** Verify: Both services communicate

---

## ✅ Phase 5: Model Versioning & Reproducibility

### 5.1 Add Model Versioning
- [ ] **(b turn)** Create: `ml/models/versions/` directory
- [ ] **(b turn)** Modify training script to:
  - Save model with timestamp/version
  - Save training metadata (features used, accuracy)
  - Save to `ml/models/versions/v1_model.pkl`
- [ ] **(b turn)** Create: `ml/models/metadata.json` with model info

### 5.2 Add Data Versioning
- [ ] **(b turn)** Create: `ml_data/versions/` directory
- [ ] **(b turn)** Modify data creation to:
  - Save training data with timestamp
  - Track which resume/job data was used
  - Save metadata about data source

### 5.3 Document Reproducibility
- [ ] **(b turn)** Create: `ml/README.md`
- [ ] **(b turn)** Document:
  - How to train model
  - How to reproduce results
  - Model performance metrics
  - Data versions used

---

## ✅ Phase 6: Testing & Validation

### 6.1 Test ML Predictions
- [ ] **(b turn)** Create: `ml/test_predictions.py`
- [ ] **(b turn)** Write test to:
  - Load sample jobs
  - Get ML predictions
  - Compare with rule-based scores
  - Print differences
- [ ] **(b turn)** Run: `python ml/test_predictions.py`
- [ ] **(b turn)** Analyze: When does ML differ from rules?

### 6.2 Validate Model Quality
- [ ] **(b turn)** Test with new jobs from `raw/foorila raw.csv`
- [ ] **(b turn)** Check: Predictions make sense
- [ ] **(b turn)** Compare: ML scores vs. manual assessment
- [ ] **(b turn)** Document: Model strengths/weaknesses

---

## 🎯 Success Criteria

- [ ] **(b turn)** Model trained and saved
- [ ] **(b turn)** Model serves predictions in Docker
- [ ] **(b turn)** API endpoint works: `/predict`
- [ ] **(b turn)** Model accuracy > baseline (rule-based)
- [ ] **(b turn)** Docker image builds and runs
- [ ] **(b turn)** Integrated with Resume MCP

---

## 📝 Notes

**What's Different from Checklist 2:**
- Checklist 2: Uses LangChain embeddings (semantic search)
- Checklist 3: Uses trained ML model (learned patterns)
- Both can work together: Embeddings for similarity + ML for scoring

**Tech Stack:**
- scikit-learn (model training)
- Docker (containerization)
- FastAPI (model serving)
- pandas (data processing)

**Learning Outcomes:**
- ✅ Docker for ML reproducibility
- ✅ Model training pipeline
- ✅ Model serving in production
- ✅ Data versioning

---

**Last Updated:** After user request for ML filter experiment
**Status:** Ready to start Phase 1

