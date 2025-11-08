# 📋 Checklist 4: Feature Store from YAML

**Goal:** Convert your `rulebook.yaml` into a feature definition schema. Learn feature engineering, YAML-to-ML metadata mapping, and feature store patterns.

**Status:** ⬜ Not Started | 🟡 In Progress | ✅ Complete

**What You'll Learn:**
- Feature engineering
- Feature store architecture
- YAML schema design
- Feature versioning
- ML metadata management

---

## 🎯 Phase 0: Understand Feature Stores

### 0.1 Understand Feature Store Concept
- [ ] **(b turn)** Read: Feature store = Centralized place for ML features
- [ ] **(b turn)** Read: Features = Inputs to ML models (skills, keywords, etc.)
- [ ] **(b turn)** Read: Goal = Convert rulebook.yaml into structured features
- [ ] **(b turn)** Read: Benefits = Reusable features, versioning, consistency

### 0.2 Review Current Rulebook
- [ ] **(b turn)** Open: `rulebook.yaml`
- [ ] **(b turn)** Identify: Positive keywords, negative keywords, weights
- [ ] **(b turn)** Understand: How these are currently used in `match_rank.py`
- [ ] **(b turn)** Plan: How to convert to feature definitions

---

## ✅ Phase 1: Design Feature Schema

### 1.1 Create Feature Schema YAML
- [ ] **(b turn)** Create: `features/feature_schema.yaml`
- [ ] **(b turn)** Design schema with:
  - Feature name
  - Feature type (categorical, numerical, boolean)
  - Source (rulebook, resume, job)
  - Transformation (how to compute)
  - Version
- [ ] **(b turn)** Example structure:
  ```yaml
  features:
    - name: python_skill_match
      type: boolean
      source: resume
      transformation: "check if 'python' in resume.skills"
      version: "1.0"
    - name: positive_keyword_count
      type: numerical
      source: rulebook
      transformation: "count matches in job.description"
      version: "1.0"
  ```

### 1.2 Map Rulebook to Features
- [ ] **(b turn)** Create: `scripts/map_rulebook_to_features.py`
- [ ] **(b turn)** Write script to:
  - Load `rulebook.yaml`
  - Convert each keyword to feature definition
  - Convert weights to feature importance
  - Generate `features/rulebook_features.yaml`
- [ ] **(b turn)** Run: `python scripts/map_rulebook_to_features.py`
- [ ] **(b turn)** Verify: Feature definitions created

---

## ✅ Phase 2: Build Feature Store

### 2.1 Create Feature Store Structure
- [ ] **(b turn)** Create: `feature_store/` directory
- [ ] **(b turn)** Create: `feature_store/__init__.py`
- [ ] **(b turn)** Create: `feature_store/feature_registry.py`
- [ ] **(b turn)** Create: `feature_store/feature_computer.py`
- [ ] **(b turn)** Create: `feature_store/feature_cache.py`

### 2.2 Implement Feature Registry
- [ ] **(b turn)** Open: `feature_store/feature_registry.py`
- [ ] **(b turn)** Write code to:
  - Load feature schema from YAML
  - Register features with metadata
  - Query features by name/type
  - Get feature versions
- [ ] **(b turn)** Test: `python -c "from feature_store.feature_registry import *; print('OK')"`

### 2.3 Implement Feature Computer
- [ ] **(b turn)** Open: `feature_store/feature_computer.py`
- [ ] **(b turn)** Write code to:
  - Take resume + job data
  - Compute each feature from schema
  - Return feature vector (dictionary)
- [ ] **(b turn)** Test: Compute features for sample job

---

## ✅ Phase 3: Feature Engineering

### 3.1 Create Feature Transformations
- [ ] **(b turn)** Create: `feature_store/transformations.py`
- [ ] **(b turn)** Write functions for:
  - Keyword matching (from rulebook)
  - Skill overlap counting
  - Experience level matching
  - Salary range matching
  - Location matching
- [ ] **(b turn)** Test: Each transformation function

### 3.2 Create Feature Pipeline
- [ ] **(b turn)** Create: `feature_store/pipeline.py`
- [ ] **(b turn)** Write pipeline to:
  - Load resume
  - Load job
  - Compute all features
  - Return feature vector
- [ ] **(b turn)** Test: Full pipeline with sample data

---

## ✅ Phase 4: Feature Versioning

### 4.1 Add Version Management
- [ ] **(b turn)** Create: `feature_store/versions.py`
- [ ] **(b turn)** Write code to:
  - Track feature versions
  - Store feature history
  - Compare feature versions
- [ ] **(b turn)** Create: `feature_store/versions/v1.yaml`
- [ ] **(b turn)** Create: `feature_store/versions/v2.yaml` (for future changes)

### 4.2 Feature Metadata Storage
- [ ] **(b turn)** Create: `feature_store/metadata.json`
- [ ] **(b turn)** Store:
  - Feature definitions
  - Version history
  - Usage statistics
  - Last updated timestamps

---

## ✅ Phase 5: Integrate with ML Pipeline

### 5.1 Connect to Model Training
- [ ] **(b turn)** Modify: `ml/train_model.py` (from Checklist 3)
- [ ] **(b turn)** Update to:
  - Use feature store instead of manual features
  - Load features from registry
  - Compute features via pipeline
- [ ] **(b turn)** Test: Model training with feature store

### 5.2 Connect to Prediction
- [ ] **(b turn)** Modify: `ml/serve_model.py`
- [ ] **(b turn)** Update to:
  - Use feature store for feature computation
  - Ensure feature consistency
- [ ] **(b turn)** Test: Predictions use feature store

---

## ✅ Phase 6: Feature Store API

### 6.1 Create Feature Store API
- [ ] **(b turn)** Create: `feature_store/api.py`
- [ ] **(b turn)** Write FastAPI endpoints:
  - `GET /features` - List all features
  - `GET /features/{name}` - Get feature definition
  - `POST /features/compute` - Compute features for resume+job
  - `GET /features/versions` - List feature versions
- [ ] **(b turn)** Test: API endpoints work

### 6.2 Integrate with Resume MCP
- [ ] **(b turn)** Open: `server_http.py`
- [ ] **(b turn)** Add: Feature store endpoints
- [ ] **(b turn)** Add: MCP tool to get features
- [ ] **(b turn)** Test: Feature store accessible via MCP

---

## ✅ Phase 7: Documentation

### 7.1 Document Feature Schema
- [ ] **(b turn)** Create: `feature_store/README.md`
- [ ] **(b turn)** Document:
  - Feature definitions
  - How to add new features
  - Feature versioning process
  - Usage examples

### 7.2 Create Feature Catalog
- [ ] **(b turn)** Create: `feature_store/catalog.md`
- [ ] **(b turn)** List all features with:
  - Name
  - Description
  - Type
  - Source
  - Example values

---

## 🎯 Success Criteria

- [ ] **(b turn)** Feature schema defined in YAML
- [ ] **(b turn)** Feature store implemented
- [ ] **(b turn)** Features computed from rulebook.yaml
- [ ] **(b turn)** Feature versioning works
- [ ] **(b turn)** Integrated with ML pipeline
- [ ] **(b turn)** API endpoints work

---

## 📝 Notes

**What's Different:**
- Checklist 2: Uses LangChain (embeddings)
- Checklist 3: Uses ML model (scikit-learn)
- Checklist 4: Uses feature store (structured features from YAML)

**Tech Stack:**
- YAML (feature definitions)
- Python (feature computation)
- FastAPI (feature store API)
- JSON (metadata storage)

**Learning Outcomes:**
- ✅ Feature engineering patterns
- ✅ Feature store architecture
- ✅ YAML schema design
- ✅ Feature versioning

---

**Last Updated:** After user request for feature store experiment
**Status:** Ready to start Phase 1

