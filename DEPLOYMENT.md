# 🚀 AI ScamShield - Cloud Deployment Guide

This guide walks you through deploying **AI ScamShield** to the cloud so anyone can access it via a public URL (`https://...`).

---

## 🌟 Option 1: Deploy to Render (Recommended — 100% Free & Simplest)

Render hosts both your **FastAPI Backend** and **React Frontend** together in a single **free Web Service**.

### Step 1: Push Your Latest Changes to GitHub

In your project folder (`c:\Users\sanab\project\ai scamshield1`), run:
```bash
git add .
git commit -m "Configure cloud deployment for Render and Docker"
git push origin main
```

*(Your repository is: `https://github.com/sanab330/ai-scamshield`)*

---

### Step 2: Create a Web Service on Render

1. Go to [https://dashboard.render.com/](https://dashboard.render.com/) and sign up / log in with your **GitHub** account.
2. Click **New +** in the top-right corner and select **Web Service**.
3. Choose **"Build and deploy from a Git repository"** and click **Next**.
4. Select your **`ai-scamshield`** repository (if not listed, click *Configure account* to grant access to your repository).

---

### Step 3: Configure the Web Service Settings

Fill in the fields as follows:

| Setting | Value |
| :--- | :--- |
| **Name** | `ai-scamshield` (or your chosen name) |
| **Region** | Singapore, Frankfurt, or Oregon (closest to you) |
| **Branch** | `main` |
| **Root Directory** | *(leave blank)* |
| **Runtime** | **Python 3** |
| **Build Command** | `cd frontend && npm install && npm run build && cd .. && pip install -r requirements.txt` |
| **Start Command** | `uvicorn backend.app.main:app --host 0.0.0.0 --port $PORT` |
| **Instance Type** | **Free** ($0 / month) |

---

### Step 4: Add Environment Variable

Scroll down to **Environment Variables** and click **Add Environment Variable**:
- **Key**: `PYTHON_VERSION`
- **Value**: `3.12.8`

---

### Step 5: Click "Deploy Web Service"

1. Click the **Deploy Web Service** button at the bottom.
2. Render will automatically:
   - Install React dependencies (`npm install`)
   - Build the frontend bundle (`npm run build`)
   - Install FastAPI & ML dependencies (`pip install -r requirements.txt`)
   - Start the unified server (`uvicorn`)
3. When the build finishes, you will see a green **"Live"** badge!
4. Your application will be accessible at:
   `https://ai-scamshield.onrender.com` (or your custom service URL).

---

## 🐳 Option 2: Deploy with Docker (Render, Railway, Fly.io, or Koyeb)

If you prefer containerized deployment, the repository includes a multi-stage `Dockerfile`:

### On Render:
1. When creating a Web Service, choose **Docker** instead of Python.
2. Render will automatically build the `Dockerfile` and deploy it!

### On Railway:
1. Go to [railway.app](https://railway.app/).
2. Click **New Project** -> **Deploy from GitHub repo**.
3. Select `ai-scamshield`. Railway detects the `Dockerfile` and deploys automatically.

---

## ⚡ Option 3: Separate Deployments (Frontend on Vercel + Backend on Render)

If you prefer keeping Frontend and Backend completely separated:

1. **Deploy Backend to Render**:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn backend.app.main:app --host 0.0.0.0 --port $PORT`
   - Copy your Render backend URL (e.g. `https://ai-scamshield-api.onrender.com`).

2. **Deploy Frontend to Vercel**:
   - Go to [vercel.com](https://vercel.com/) and click **Add New Project**.
   - Import your GitHub repo.
   - Set **Root Directory** to `frontend`.
   - Add Environment Variable:
     - `VITE_API_BASE_URL` = `https://ai-scamshield-api.onrender.com/api`
   - Click **Deploy**.

---

## 🛠️ Verifying Your Deployment

Once deployed, visit your live URL:
- **Web UI**: Open `https://your-service-name.onrender.com` to test all scanner modules (Message Scanner, URL Phishing Scanner, Risk Simulator, etc.).
- **Interactive Swagger API Docs**: Open `https://your-service-name.onrender.com/docs`.
- **Health Check**: Open `https://your-service-name.onrender.com/api/health`.
