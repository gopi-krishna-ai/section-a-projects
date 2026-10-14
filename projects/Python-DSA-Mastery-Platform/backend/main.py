import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from backend.config import settings
from backend.database import engine, Base, SessionLocal
from backend.services.seed_data import seed_database

from backend.routes.auth import router as auth_router
from backend.routes.curriculum import router as curriculum_router
from backend.routes.problems import router as problems_router
from backend.routes.execution import router as execution_router
from backend.routes.mistakes import router as mistakes_router
from backend.routes.revisions import router as revisions_router
from backend.routes.debug_lab import router as debug_lab_router
from backend.routes.logic_gym import router as logic_gym_router
from backend.routes.analytics import router as analytics_router

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Advanced Python, Logical Thinking & DSA Mastery Platform API",
    version="2.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(auth_router)
app.include_router(curriculum_router)
app.include_router(problems_router)
app.include_router(execution_router)
app.include_router(mistakes_router)
app.include_router(revisions_router)
app.include_router(debug_lab_router)
app.include_router(logic_gym_router)
app.include_router(analytics_router)

@app.on_event("startup")
def startup_event():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        seed_database(db)
        print("Database initialized and curriculum seeded successfully.")
    finally:
        db.close()

@app.get("/api/health")
def health_check():
    return {
        "status": "healthy",
        "app": settings.PROJECT_NAME,
        "execution_engine": "isolated_subprocess",
        "version": "2.0.0"
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
