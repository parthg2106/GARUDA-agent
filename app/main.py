"""Main FastAPI application entry point."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging

from app.config import settings
from app.api.routes import router
from app.utils.logger import logger

# Initialize FastAPI app
app = FastAPI(
    title=settings.API_TITLE,
    version=settings.APP_VERSION,
    description="GARUDA - Autonomous Swarm Coordination & Mission Execution Agent",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Include routes
app.include_router(router)


@app.on_event("startup")
async def startup_event():
    """Run on app startup."""
    logger.info(f"{settings.APP_NAME} v{settings.APP_VERSION} starting up...")
    logger.info(f"Environment: {settings.ENVIRONMENT}")
    logger.info(f"Debug mode: {settings.DEBUG}")


@app.on_event("shutdown")
async def shutdown_event():
    """Run on app shutdown."""
    logger.info(f"{settings.APP_NAME} shutting down...")


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "docs": "/api/docs",
        "status": "operational"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    )
