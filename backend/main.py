"""
CodeSage Backend - AI-Powered Code Understanding Platform
Main FastAPI application entry point
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import os
from pathlib import Path
from dotenv import load_dotenv

from app.api.routes import router
from app.core.config import settings
from app.core.logging import setup_logging

# Load .env from current directory or parent directory (for consistency with config)
env_path = Path(".env")
if not env_path.exists():
    env_path = Path("..") / ".env"
    if not env_path.exists():
        # Try going up from backend/ to root
        env_path = Path(__file__).parent.parent / ".env"

if env_path.exists():
    load_dotenv(env_path)
else:
    # Fallback: try default location
    load_dotenv()

logger = setup_logging()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    logger.info("Starting CodeSage Backend...")
    yield
    logger.info("Shutting down CodeSage Backend...")


app = FastAPI(
    title="CodeSage API",
    description="AI-Powered Code Understanding and Documentation Platform",
    version="1.0.0",
    lifespan=lifespan
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(router, prefix="/api/v1")


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "message": "CodeSage API is running",
        "version": "1.0.0",
        "status": "healthy"
    }


@app.get("/health")
async def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "service": "codesage-backend",
        "version": "1.0.0"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=True
    )

