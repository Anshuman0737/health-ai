# Hybrid Preventive Intelligence System

**Version:** 2.0.0  
**Type:** Multi-Domain Preventive Risk Intelligence Engine  
**Backend:** FastAPI (Python)  
**Architecture:** Modular Service-Based  

---

## 🚀 Overview

Hybrid Preventive Intelligence System is an AI-driven, multi-domain health risk modeling platform that:

- Extracts biomarkers from medical reports (PDF)
- Computes domain-weighted preventive risk scores
- Applies abnormality escalation logic
- Models volatility using Monte Carlo simulation
- Performs scenario comparison (Risk Delta Engine)
- Estimates compliance probability
- Projects 5-year and 10-year risk envelopes
- Quantifies economic impact
- Generates executive-grade summaries

This is not a static scoring tool.  
It is a preventive intelligence engine.

---

## 🧠 Core Capabilities

### 1️⃣ Deterministic Multi-Domain Risk Engine

Risk domains include:

- Liver Risk  
- Cardiometabolic Risk  
- Inflammatory Load  
- Metabolic Instability  
- Nutritional Deficiency  
- Mental Resilience  

Each domain is normalized and weighted into a composite risk score.

---

### 2️⃣ Abnormality Escalation Override

High-severity markers automatically elevate the risk floor:

- ALT > 200  
- hs-CRP > 3  
- HbA1c ≥ 5.7  

This prevents false "Low Risk" classification.

---

### 3️⃣ Monte Carlo Volatility Modeling

Risk is not static.

We simulate stochastic fluctuation to generate:

- Mean projection  
- 10th percentile band  
- 90th percentile band  

Outputs:

- 5-year risk envelope  
- 10-year risk envelope  

---

### 4️⃣ Risk Delta Engine (Scenario Modeling)

Allows simulation of improved biomarker states.

Example interventions:

- Reduce LDL  
- Normalize ALT  
- Lower hs-CRP  
- Correct Vitamin D deficiency  
- Improve stress levels  
- Optimize sleep  

Outputs:

- Absolute risk reduction  
- Relative percent change  
- Trajectory direction  
- Intervention impact magnitude  

---

### 5️⃣ Compliance Probability Modeling

Compliance probability is estimated from:

- Stress level  
- Sleep quality  
- Resilience index  

Used to model intervention realism.

---

### 6️⃣ Economic Impact Modeling

Translates risk into:

- Estimated annual health burden  
- 10-year projected cost  
- Preventable opportunity  

Supports insurer and employer use cases.

---

## 🏗 Architecture
backend/
│
├── app/
│ ├── main.py
│ ├── routes/
│ │ └── report_routes.py
│ └── services/
│ ├── biomarker_extractor.py
│ ├── risk_engine.py
│ ├── intervention_engine.py
│ ├── ai_report_engine.py
│ └── clinical_summary.py




### Service Responsibilities

| File | Responsibility |
|------|---------------|
| biomarker_extractor.py | PDF parsing + biomarker extraction |
| risk_engine.py | Multi-domain scoring logic |
| intervention_engine.py | ROI + delta computation |
| ai_report_engine.py | Executive summary generation |
| clinical_summary.py | Mechanistic interpretation |
| report_routes.py | API endpoints |

---

## ⚙ Installation (Run From Scratch)

### 1️⃣ Clone Repository

git clone https://github.com/Anshuman0737/health-ai.git
cd health-ai

2️⃣ Create Virtual Environment

Windows

python -m venv venv
venv\Scripts\activate

Mac/Linux

python3 -m venv venv
source venv/bin/activate
3️⃣ Install Dependencies

If requirements.txt exists:

pip install -r requirements.txt

If not:

pip install fastapi uvicorn pdfplumber numpy
4️⃣ Run Backend
cd backend
uvicorn app.main:app --reload

Server runs at:

http://127.0.0.1:8000

API documentation:

http://127.0.0.1:8000/docs
📡 API Endpoints
🔹 POST /upload-report

Upload medical report (PDF).

Returns:

Extracted biomarkers

Risk score

Risk vector

Volatility index

5-year / 10-year projections

Compliance probability

Economic impact model

Executive summary

🔹 POST /simulate-risk

Simulate improved biomarker states.

Query Parameters (optional):

ldl

triglycerides

alt

hs_crp

vitamin_d

stress_level

sleep_hours

Returns:

Baseline risk

Simulated risk

Risk delta

Trajectory direction

Updated projections

Intervention ROI

Executive summary

📊 Example Workflow

Upload baseline blood report.

Receive systemic risk classification.

Simulate normalization of liver enzymes.

Quantify projected 10-year risk reduction.

Estimate preventable economic burden.

⚠ Intended Use

This system is designed for:

Preventive awareness modeling

Risk simulation experimentation

Research prototyping

Hackathon demonstration

Concept validation

Not intended for clinical diagnosis.

🏆 Competitive Differentiators

Multi-domain synergy modeling

Escalation override logic

Monte Carlo projection bands

Intervention ROI engine

Compliance-aware modeling

Economic translation layer

Executive-grade narrative synthesis

🔮 Future Roadmap

Nonlinear longitudinal modeling

Employer cohort analytics

Risk clustering

Adaptive learning layer

Cloud deployment (Docker + CI/CD)
