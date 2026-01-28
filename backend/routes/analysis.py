"""
API routes for analysis
"""
from fastapi import APIRouter, BackgroundTasks, HTTPException
from typing import List, Optional

from core.logger import logger
from models.schemas import (
    AnalysisRequest,
    AnalysisResponse,
    AnalysisStatusResponse,
    AnalysisResults,
    AnalysisStatus,
)
from services.orchestrator import orchestrator

router = APIRouter(prefix="/api", tags=["Analysis"])


@router.post("/analyze", response_model=AnalysisResponse)
async def start_analysis(
    request: AnalysisRequest,
    background_tasks: BackgroundTasks
):
    """
    Start a new repository analysis
    
    - **repository_url**: GitHub repository URL
    - **github_token**: GitHub personal access token
    - **analyzers**: Optional list of specific analyzers to run
    - **ai_provider**: AI provider to use (anthropic or openai)
    """
    try:
        # Create analysis
        analysis_id = orchestrator.create_analysis(
            repository_url=str(request.repository_url),
            github_token=request.github_token,
            analyzers=request.analyzers,
            ai_provider=request.ai_provider or "anthropic"
        )
        
        # Run analysis in background
        background_tasks.add_task(orchestrator.run_analysis, analysis_id)
        
        # Get initial status
        status_info = orchestrator.get_analysis_status(analysis_id)
        
        return AnalysisResponse(
            analysis_id=analysis_id,
            status=status_info["status"],
            created_at=status_info["started_at"] or orchestrator.analyses[analysis_id]["created_at"],
            repository_url=str(request.repository_url)
        )
        
    except Exception as e:
        logger.error(f"Failed to start analysis: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/analysis/{analysis_id}/status", response_model=AnalysisStatusResponse)
async def get_analysis_status(analysis_id: str):
    """
    Get the status of an analysis
    
    - **analysis_id**: Unique analysis identifier
    """
    try:
        status_info = orchestrator.get_analysis_status(analysis_id)
        return AnalysisStatusResponse(**status_info)
        
    except Exception as e:
        logger.error(f"Failed to get analysis status: {e}")
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/analysis/{analysis_id}/results", response_model=AnalysisResults)
async def get_analysis_results(analysis_id: str):
    """
    Get the results of a completed analysis
    
    - **analysis_id**: Unique analysis identifier
    """
    try:
        results = orchestrator.get_analysis_results(analysis_id)
        return results
        
    except Exception as e:
        logger.error(f"Failed to get analysis results: {e}")
        raise HTTPException(status_code=404, detail=str(e))
