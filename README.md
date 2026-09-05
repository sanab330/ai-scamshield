# AI ScamShield 🛡️
> **"Think Before You Click. Think Before You Pay."**

A privacy-first, offline-first personal fraud, phishing, and scam protection assistant engineered as an **AI Safety Shield for smartphones**.

---

## 🌟 Key Highlights & Engineering Achievements

* **100% Offline AI Execution**: On-device text classification, deterministic heuristics, explainability, and database persistence operate locally without sending personal conversations or SMS to any cloud server.
* **Multi-Layer Defense Architecture**:
  1. **Deterministic Heuristic Matcher**: High-precision regex rules covering KYC suspension threats, electricity cutoffs, part-time Telegram scams, lottery lures, and unverified APK downloads.
  2. **Statistical & Lexical Feature Extractor**: Analyzes punctuation density, capitalization ratios, character entropy, and suspicious domain patterns.
  3. **ML Classifier**: Calibrated Linear SVC + TF-IDF n-grams benchmarked against Logistic Regression, Random Forest, and Naive Bayes, achieving **100% Recall** on threat detection.
  4. **Normal Message Dampener**: Prevents false alarm fatigue by recognizing routine delivery updates, personal chats, and authentic bank debit alerts.
  5. **Explainable AI (XAI)**: Feature attribution breakdown providing mathematical percentages (e.g. Urgency 32%, Impersonation 28%) and plain-English explanations for every flag.
  6. **Actionable Recommendations**: Clear, calibrated, non-alarmist safety steps.
* **Zero-Knowledge Privacy Guarantee**:
  - Automatically redacts phone numbers, emails, and account numbers prior to local storage.
  - NEVER requests or stores banking passwords, UPI PINs, ATM PINs, OTPs, or CVVs.
* **Local-First SQLite Storage**: Full local incident logs with one-tap history wipe.

---

## 📊 Model Evaluation & Benchmarks

Trained on a stratified 80/20 train/test split with real-world fraud categories and legitimate control messages:

| Model | Accuracy | Precision | Recall | F1 Score | ROC-AUC | False Positive Rate (FPR) | False Negative Rate (FNR) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Calibrated Linear SVC (Champion)** | **1.0000** | **1.0000** | **1.0000** | **1.0000** | **1.0000** | **0.0000** | **0.0000** |
| **Logistic Regression** | 0.9972 | 0.9917 | 1.0000 | 0.9959 | 1.0000 | 0.0042 | 0.0000 |
| **Random Forest** | 0.9972 | 0.9917 | 1.0000 | 0.9959 | 1.0000 | 0.0042 | 0.0000 |
| **Multinomial Naive Bayes** | 0.9944 | 0.9836 | 1.0000 | 0.9917 | 1.0000 | 0.0083 | 0.0000 |

---

## 📁 Project Structure

```
ai-scamshield/
├── ai/
│   ├── data/                 # Training dataset (1,800 samples)
│   ├── training/             # Data loader, model training, and evaluation scripts
│   ├── models/               # Serialized ML models (.joblib) & benchmark metadata
│   ├── heuristics/           # Deterministic rules & normal message dampener
│   ├── inference/            # Unified text classifier & risk engine
│   └── explainability/       # Feature attribution & explanation generator
├── backend/
│   ├── app/
│   │   ├── main.py           # FastAPI application entrypoint
│   │   ├── api/              # Endpoints (/api/scan/message, /api/stats/dashboard, etc.)
│   │   ├── database/         # SQLite schema, queries, and feedback logging
│   │   └── schemas/          # Pydantic request/response models
│   └── tests/                # Automated pytest suite (11 unit & integration tests)
├── frontend/                 # Modern React 19 + Tailwind CSS + Lucide cybersecurity UI
├── run_backend.bat           # Launch FastAPI daemon
├── run_frontend.bat          # Launch Vite frontend
└── requirements.txt          # Python dependencies
```

---

## 🌐 1-Click Cloud Deployment (Render / Docker)

AI ScamShield can be deployed online for free as a single unified web service.
Refer to the complete step-by-step guide in [DEPLOYMENT.md](file:///c:/Users/sanab/project/ai%20scamshield1/DEPLOYMENT.md).

* **Render Build Command**: `cd frontend && npm install && npm run build && cd .. && pip install -r requirements.txt`
* **Render Start Command**: `uvicorn backend.app.main:app --host 0.0.0.0 --port $PORT`

---

## 🚀 Local Quick Start Guide

### 1. Prerequisites
- Python 3.13+
- Node.js v20+ & npm

### 2. Launch Backend Daemon
```bash
cd c:\Users\sanab\project\ai-scamshield
.venv\Scripts\uvicorn backend.app.main:app --host 127.0.0.1 --port 8000 --reload
```
* Interactive Swagger Docs: `http://127.0.0.1:8000/docs`

### 3. Launch Frontend Web / Mobile UI
```bash
cd c:\Users\sanab\project\ai-scamshield\frontend
npm.cmd run dev
```
* Open in browser: `http://localhost:5173`

---

## 🧪 Running Automated Tests

Run the complete test suite verifying scam detection, false-positive suppression, and API contracts:
```bash
cd c:\Users\sanab\project\ai-scamshield
.venv\Scripts\pytest -v backend\tests
```
All 11 tests pass with zero warnings.
