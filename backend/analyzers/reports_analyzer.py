"""
Reports analyzer - Generates code quality and analysis reports
"""
from typing import Dict, Any
from .base import BaseAnalyzer
from models.schemas import Reports


class ReportsAnalyzer(BaseAnalyzer):
    """Analyzer for generating code quality and analysis reports"""
    
    async def analyze(self) -> Reports:
        """
        Generate analysis reports
        
        Returns:
            Reports with code quality metrics and recommendations
        """
        self.log_start()
        
        # Use AI service's code quality analysis
        result = await self.ai_service.analyze_code_quality(self.repo_data)
        
        # Parse result into Reports model
        reports = Reports(
            code_quality_score=result.get("code_quality_score", 75.0),
            code_metrics=result.get("code_metrics", {}),
            technical_debt=result.get("technical_debt", {}),
            security_issues=result.get("security_issues", []),
            performance_analysis=result.get("performance_analysis", {}),
            recommendations=result.get("recommendations", [])
        )
        
        self.log_complete()
        return reports
