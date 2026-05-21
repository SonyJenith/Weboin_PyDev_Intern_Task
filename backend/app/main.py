from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path

from .database import init_db
from .routers import auth, tasks

app = FastAPI(title="Task Manager API", version="1.0.0")

# Configure CORS
cors_origins = [
    "http://localhost:3000",
    "http://localhost:8001",
    "http://localhost:8000",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:8001",
    "http://127.0.0.1:8000",
    "https://sonyjenith-d-weboin-pydev-intern-task.onrender.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
    max_age=3600,
)

# Include routers
app.include_router(auth.router)
app.include_router(tasks.router)

# Serve static frontend files
frontend_path = Path(__file__).parent.parent.parent / "frontend"
if frontend_path.exists():
    app.mount("/", StaticFiles(directory=str(frontend_path), html=True), name="frontend")


@app.on_event("startup")
def startup_event():
    """Initialize database on startup."""
    init_db()
