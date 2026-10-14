import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from backend.config import settings
from backend.database import engine, Base, SessionLocal
from backend.models import Question
from backend.ingestion.seed_data import run_ingestion
from backend.services.auth import seed_demo_accounts

from backend.routes.auth import router as auth_router
from backend.routes.topics import router as topics_router
from backend.routes.questions import router as questions_router
from backend.routes.sessions import router as sessions_router
from backend.routes.mistakes import router as mistakes_router
from backend.routes.revisions import router as revisions_router
from backend.routes.analytics import router as analytics_router
from backend.routes.mock_tests import router as mock_tests_router

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Intelligent AI Aptitude Mastery Coach API for placement preparation",
    version="1.0.0"
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include All Routers
app.include_router(auth_router)
app.include_router(topics_router)
app.include_router(questions_router)
app.include_router(sessions_router)
app.include_router(mistakes_router)
app.include_router(revisions_router)
app.include_router(analytics_router)
app.include_router(mock_tests_router)

@app.on_event("startup")
def startup_event():
    # Ensure tables exist and data is ingested
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    q_count = db.query(Question).count()
    if q_count < 1800:
        print(f"Detected {q_count} questions in DB. Running repository ingestion...")
        run_ingestion()
    else:
        print(f"Verified database loaded with {q_count} questions.")
    
    # Seed demo accounts
    seed_demo_accounts(db)
    print("Demo accounts initialized (Rohan, Priya, Alex, Demo Learner).")
    db.close()

@app.get("/api/health")
def health_check():
    return {
        "status": "healthy",
        "app": settings.PROJECT_NAME,
        "database": "connected"
    }

# Mount Frontend SPA for single-port deployment & Cloudflare tunnel
frontend_dist = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'frontend', 'dist'))
if os.path.exists(frontend_dist):
    assets_dir = os.path.join(frontend_dist, "assets")
    if os.path.exists(assets_dir):
        app.mount("/assets", StaticFiles(directory=assets_dir), name="assets")

    @app.get("/{full_path:path}")
    async def serve_spa(full_path: str):
        if full_path.startswith("api"):
            raise HTTPException(status_code=404, detail="API endpoint not found")
        file_path = os.path.join(frontend_dist, full_path)
        if os.path.exists(file_path) and os.path.isfile(file_path):
            return FileResponse(file_path)
        return FileResponse(os.path.join(frontend_dist, "index.html"))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
