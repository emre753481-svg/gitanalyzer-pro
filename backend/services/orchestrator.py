"""
Analysis orchestration service
"""
import asyncio
import uuid
from datetime import datetime
from typing import Dict, Any, List, Optional
from pathlib import Path
import json

from core.logger import logger
from core.config import settings
from core.exceptions import AnalysisException
from models.schemas import (
    AnalysisStatus,
    AnalyzerType,
    AnalysisResults,
)
from services import GitHubService, AIService, parse_github_url
from analyzers import (
    ScopeAnalyzer,
    UMLAnalyzer,
    BPMNAnalyzer,
    FlowAnalyzer,
    BusinessAnalyzer,
    RequirementsAnalyzer,
    ArchitectureAnalyzer,
    ReportsAnalyzer,
)


class AnalysisOrchestrator:
    """Orchestrates the complete analysis process"""
    
    def __init__(self):
        """Initialize orchestrator"""
        self.analyses: Dict[str, Dict[str, Any]] = {}
        self.results_dir = Path(settings.ANALYSIS_RESULTS_DIR)
        self.results_dir.mkdir(parents=True, exist_ok=True)
    
    def create_analysis(
        self,
        repository_url: str,
        github_token: str,
        analyzers: Optional[List[AnalyzerType]] = None,
        ai_provider: str = "anthropic"
    ) -> str:
        """
        Create a new analysis
        
        Args:
            repository_url: GitHub repository URL
            github_token: GitHub access token
            analyzers: List of analyzers to run (None = all)
            ai_provider: AI provider to use
            
        Returns:
            Analysis ID
        """
        analysis_id = str(uuid.uuid4())
        
        self.analyses[analysis_id] = {
            "id": analysis_id,
            "repository_url": repository_url,
            "github_token": github_token,
            "analyzers": analyzers or list(AnalyzerType),
            "ai_provider": ai_provider,
            "status": AnalysisStatus.PENDING,
            "progress": 0,
            "current_step": None,
            "created_at": datetime.now(),
            "started_at": None,
            "completed_at": None,
            "error": None,
            "results": None,
        }
        
        logger.info(f"Created analysis {analysis_id} for {repository_url}")
        return analysis_id
    
    async def run_analysis(self, analysis_id: str):
        """
        Run the complete analysis asynchronously
        
        Args:
            analysis_id: Analysis ID
        """
        analysis = self.analyses.get(analysis_id)
        if not analysis:
            raise AnalysisException(f"Analysis {analysis_id} not found")
        
        try:
            # Update status
            analysis["status"] = AnalysisStatus.PROCESSING
            analysis["started_at"] = datetime.now()
            
            # Step 1: Fetch repository data
            analysis["current_step"] = "Fetching repository data"
            analysis["progress"] = 10
            logger.info(f"[{analysis_id}] Fetching repository data")
            
            owner, repo = parse_github_url(analysis["repository_url"])
            github_service = GitHubService(analysis["github_token"])
            repo_data = await github_service.analyze_repository(owner, repo)
            
            # Step 2: Initialize AI service
            analysis["current_step"] = "Initializing AI service"
            analysis["progress"] = 20
            logger.info(f"[{analysis_id}] Initializing AI service")
            
            ai_service = AIService(provider=analysis["ai_provider"])
            
            # Step 3: Run analyzers
            results = await self._run_analyzers(
                analysis_id,
                analysis,
                repo_data,
                ai_service
            )
            
            # Step 4: Save results
            analysis["current_step"] = "Saving results"
            analysis["progress"] = 95
            logger.info(f"[{analysis_id}] Saving results")
            
            results_path = self.results_dir / f"{analysis_id}.json"
            with open(results_path, "w", encoding="utf-8") as f:
                json.dump(results.model_dump(), f, indent=2, default=str)
            
            # Complete
            analysis["status"] = AnalysisStatus.COMPLETED
            analysis["progress"] = 100
            analysis["current_step"] = "Completed"
            analysis["completed_at"] = datetime.now()
            analysis["results"] = results
            
            logger.info(f"[{analysis_id}] Analysis completed successfully")
            
        except Exception as e:
            logger.error(f"[{analysis_id}] Analysis failed: {e}")
            analysis["status"] = AnalysisStatus.FAILED
            analysis["error"] = str(e)
            analysis["completed_at"] = datetime.now()
            raise
    
    async def _run_analyzers(
        self,
        analysis_id: str,
        analysis: Dict[str, Any],
        repo_data: Dict[str, Any],
        ai_service: AIService
    ) -> AnalysisResults:
        """
        Run all specified analyzers
        
        Args:
            analysis_id: Analysis ID
            analysis: Analysis metadata
            repo_data: Repository data
            ai_service: AI service instance
            
        Returns:
            Complete analysis results
        """
        analyzers_to_run = analysis["analyzers"]
        total_analyzers = len(analyzers_to_run)
        
        results = AnalysisResults(
            analysis_id=analysis_id,
            repository_url=analysis["repository_url"],
            analyzed_at=datetime.now()
        )
        
        # Mapping of analyzer types to classes
        analyzer_map = {
            AnalyzerType.SCOPE: ("scope_document", ScopeAnalyzer),
            AnalyzerType.UML: ("uml_diagrams", UMLAnalyzer),
            AnalyzerType.BPMN: ("bpmn_diagrams", BPMNAnalyzer),
            AnalyzerType.FLOW: ("flow_diagrams", FlowAnalyzer),
            AnalyzerType.BUSINESS: ("business_analysis", BusinessAnalyzer),
            AnalyzerType.REQUIREMENTS: ("requirements", RequirementsAnalyzer),
            AnalyzerType.ARCHITECTURE: ("architecture", ArchitectureAnalyzer),
            AnalyzerType.REPORTS: ("reports", ReportsAnalyzer),
        }
        
        for idx, analyzer_type in enumerate(analyzers_to_run):
            field_name, analyzer_class = analyzer_map[analyzer_type]
            
            analysis["current_step"] = f"Running {analyzer_type.value} analyzer"
            analysis["progress"] = 20 + int((idx / total_analyzers) * 70)
            
            logger.info(f"[{analysis_id}] Running {analyzer_type.value} analyzer")
            
            try:
                analyzer = analyzer_class(ai_service, repo_data)
                result = await analyzer.analyze()
                setattr(results, field_name, result)
                
            except Exception as e:
                logger.error(f"[{analysis_id}] {analyzer_type.value} analyzer failed: {e}")
                # Continue with other analyzers even if one fails
                continue
        
        return results
    
    def get_analysis_status(self, analysis_id: str) -> Dict[str, Any]:
        """
        Get analysis status
        
        Args:
            analysis_id: Analysis ID
            
        Returns:
            Status information
        """
        analysis = self.analyses.get(analysis_id)
        if not analysis:
            raise AnalysisException(f"Analysis {analysis_id} not found")
        
        return {
            "analysis_id": analysis_id,
            "status": analysis["status"],
            "progress_percentage": analysis["progress"],
            "current_step": analysis["current_step"],
            "started_at": analysis["started_at"],
            "completed_at": analysis["completed_at"],
            "error_message": analysis["error"],
        }
    
    def get_analysis_results(self, analysis_id: str) -> AnalysisResults:
        """
        Get analysis results
        
        Args:
            analysis_id: Analysis ID
            
        Returns:
            Analysis results
        """
        analysis = self.analyses.get(analysis_id)
        if not analysis:
            raise AnalysisException(f"Analysis {analysis_id} not found")
        
        if analysis["status"] != AnalysisStatus.COMPLETED:
            raise AnalysisException(f"Analysis {analysis_id} is not completed yet")
        
        # Load from file if not in memory
        if not analysis["results"]:
            results_path = self.results_dir / f"{analysis_id}.json"
            if results_path.exists():
                with open(results_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    analysis["results"] = AnalysisResults(**data)
        
        return analysis["results"]


# Global orchestrator instance
orchestrator = AnalysisOrchestrator()
