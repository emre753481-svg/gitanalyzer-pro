"""
API routes for export functionality
"""
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from datetime import datetime, timedelta
from pathlib import Path

from core.logger import logger
from models.schemas import ExportRequest, ExportResponse, ExportFormat
from services.orchestrator import orchestrator
from services.export_service import ExportService

router = APIRouter(prefix="/api", tags=["Export"])
export_service = ExportService()


@router.post("/export/{analysis_id}/{format}", response_model=ExportResponse)
async def export_analysis(
    analysis_id: str,
    format: ExportFormat,
    include_diagrams: bool = True
):
    """
    Export analysis results in specified format
    
    - **analysis_id**: Unique analysis identifier
    - **format**: Export format (pdf, markdown, json)
    - **include_diagrams**: Whether to include diagram images
    """
    try:
        # Get analysis results
        results = orchestrator.get_analysis_results(analysis_id)
        
        # Export based on format
        if format == ExportFormat.JSON:
            file_path = await export_service.export_to_json(analysis_id, results)
        elif format == ExportFormat.MARKDOWN:
            file_path = await export_service.export_to_markdown(analysis_id, results, include_diagrams)
        elif format == ExportFormat.PDF:
            file_path = await export_service.export_to_pdf(analysis_id, results, include_diagrams)
        else:
            raise HTTPException(status_code=400, detail=f"Unsupported format: {format}")
        
        # Get file size
        file_size = export_service.get_file_size(file_path)
        
        # Generate download URL
        download_url = export_service.generate_download_url(analysis_id, format)
        
        return ExportResponse(
            download_url=download_url,
            file_size_bytes=file_size,
            format=format,
            expires_at=datetime.now() + timedelta(hours=24)
        )
        
    except Exception as e:
        logger.error(f"Failed to export analysis: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/download/{analysis_id}/{format}")
async def download_export(analysis_id: str, format: str):
    """
    Download exported file
    
    - **analysis_id**: Unique analysis identifier
    - **format**: File format (pdf, markdown, json)
    """
    try:
        results_dir = Path(export_service.results_dir)
        file_path = results_dir / f"{analysis_id}.{format}"
        
        if not file_path.exists():
            raise HTTPException(status_code=404, detail="Export file not found")
        
        # Determine media type
        media_types = {
            "pdf": "application/pdf",
            "markdown": "text/markdown",
            "md": "text/markdown",
            "json": "application/json"
        }
        
        media_type = media_types.get(format, "application/octet-stream")
        
        return FileResponse(
            path=file_path,
            media_type=media_type,
            filename=f"gitanalyzer-{analysis_id}.{format}"
        )
        
    except Exception as e:
        logger.error(f"Failed to download export: {e}")
        raise HTTPException(status_code=404, detail=str(e))
