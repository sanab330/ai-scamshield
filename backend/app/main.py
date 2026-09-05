"""
AI ScamShield - FastAPI Backend Application Entrypoint.
Offline-First Edge AI Daemon for Personal Fraud & Scam Protection.
"""

import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from contextlib import asynccontextmanager

from backend.app.database.models import init_db
from backend.app.api.routes_scan import router as scan_router
from backend.app.api.routes_url import router as url_router
from backend.app.api.routes_conversation import router as conv_router
from backend.app.api.routes_payment import router as payment_router
from backend.app.api.routes_profile import router as profile_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize SQLite database on startup
    init_db()
    print("[AI ScamShield] Local SQLite Database Initialized.")
    yield
    print("[AI ScamShield] Daemon Shutting Down.")

app = FastAPI(
    title="AI ScamShield API",
    description="Privacy-First, Offline-First AI Safety Shield for Scam, Phishing, and Fraud Protection.",
    version="1.0.0",
    lifespan=lifespan
)

# Enable CORS for Frontend Development & Mobile WebViews
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register All Routers under /api
app.include_router(scan_router, prefix="/api", tags=["Message Scanner"])
app.include_router(url_router, prefix="/api", tags=["URL & Phishing Scanner"])
app.include_router(conv_router, prefix="/api", tags=["Conversation Analyzer"])
app.include_router(payment_router, prefix="/api", tags=["Payment Shield & Simulator"])
app.include_router(profile_router, prefix="/api", tags=["Profile Inspector"])

@app.get("/api")
@app.get("/api/health")
def api_status():
    return {
        "app": "AI ScamShield",
        "tagline": "Think Before You Click. Think Before You Pay.",
        "status": "ONLINE / CLOUD DEPLOYED",
        "privacy": "Zero-Knowledge Local Processing",
        "modules": [
            "AI Message Scanner",
            "Scam Conversation Analyzer & Early Warning",
            "Structural URL Scanner",
            "Payment Risk Manager & Stop Before You Pay",
            "What-If Risk Simulator",
            "Social Media Profile Inspector",
            "Emergency Safety Mode"
        ],
        "version": "1.0.0"
    }

# Static Frontend Serving for Production / Cloud Deployment
FRONTEND_DIST = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "frontend", "dist"))

if os.path.exists(FRONTEND_DIST):
    assets_dir = os.path.join(FRONTEND_DIST, "assets")
    if os.path.isdir(assets_dir):
        app.mount("/assets", StaticFiles(directory=assets_dir), name="assets")

    @app.get("/")
    async def serve_spa():
        index_file = os.path.join(FRONTEND_DIST, "index.html")
        if os.path.exists(index_file):
            return FileResponse(index_file)
        return api_status()

    @app.get("/{full_path:path}")
    async def serve_spa_catch_all(full_path: str):
        # Allow API routes and documentation to pass through
        if full_path.startswith(("api", "docs", "openapi.json", "redoc")):
            raise HTTPException(status_code=404, detail="Not Found")
        
        file_path = os.path.join(FRONTEND_DIST, full_path)
        if os.path.isfile(file_path):
            return FileResponse(file_path)
        
        index_file = os.path.join(FRONTEND_DIST, "index.html")
        if os.path.exists(index_file):
            return FileResponse(index_file)
        raise HTTPException(status_code=404, detail="File Not Found")
else:
    @app.get("/")
    def root():
        return api_status()

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("backend.app.main:app", host="0.0.0.0", port=port, reload=False)

