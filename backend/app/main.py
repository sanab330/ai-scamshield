"""
AI ScamShield - FastAPI Backend Application Entrypoint.
Offline-First Edge AI Daemon for Personal Fraud & Scam Protection.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
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

@app.get("/")
def root():
    return {
        "app": "AI ScamShield",
        "tagline": "Think Before You Click. Think Before You Pay.",
        "status": "ONLINE / LOCAL DAEMON ACTIVE",
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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.app.main:app", host="127.0.0.1", port=8000, reload=True)
