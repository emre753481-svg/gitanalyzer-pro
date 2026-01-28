"""
GitAnalyzer Pro - FastAPI Main Application
"""
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from datetime import datetime
from contextlib import asynccontextmanager

from core.config import settings
from core.logger import logger
from core.exceptions import GitAnalyzerException
from models.schemas import HealthCheck
from routes import analysis, export


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    logger.info("🚀 GitAnalyzer Pro starting up...")
    logger.info(f"AI Provider: {settings.AI_PROVIDER}")
    logger.info(f"Debug Mode: {settings.DEBUG}")
    yield
    logger.info("🛑 GitAnalyzer Pro shutting down...")


# Create FastAPI app
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.API_VERSION,
    description="""
    GitAnalyzer Pro - Enterprise-level GitHub Repository Analysis Platform
    
    ## Features
    - 🔍 Comprehensive repository analysis
    - 🤖 AI-powered documentation generation
    - 📊 UML, BPMN, and Flow diagrams
    - 💼 Business analysis and requirements
    - 🏗️ Architecture documentation
    - 📈 Code quality reports
    - 📥 Export to PDF, Markdown, JSON
    
    ## Workflow
    1. POST /api/analyze - Start analysis
    2. GET /api/analysis/{id}/status - Check progress
    3. GET /api/analysis/{id}/results - Get results
    4. POST /api/export/{id}/{format} - Export results
    """,
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)


# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.get_cors_origins(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Exception handler
@app.exception_handler(GitAnalyzerException)
async def gitanalyzer_exception_handler(request: Request, exc: GitAnalyzerException):
    """Handle custom GitAnalyzer exceptions"""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.__class__.__name__,
            "message": exc.message,
            "timestamp": datetime.now().isoformat()
        }
    )


# Health check endpoint
@app.get("/", response_model=HealthCheck, tags=["Health"])
async def health_check():
    """
    Health check endpoint
    
    Returns the current status and version of the API
    """
    return HealthCheck(
        status="healthy",
        version=settings.API_VERSION,
        timestamp=datetime.now(),
        services={
            "github_api": "operational",
            "ai_service": settings.AI_PROVIDER,
            "export_service": "operational"
        }
    )


# Include routers
app.include_router(analysis.router)
app.include_router(export.router)


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
        log_level=settings.LOG_LEVEL.lower()
    )
