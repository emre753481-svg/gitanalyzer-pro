"""
Business analyzer - Generates business analysis documents
"""
from typing import Dict, Any
from .base import BaseAnalyzer
from models.schemas import BusinessAnalysis


class BusinessAnalyzer(BaseAnalyzer):
    """Analyzer for generating business analysis documents"""
    
    async def analyze(self) -> BusinessAnalysis:
        """
        Generate business analysis
        
        Returns:
            BusinessAnalysis with SWOT, ROI, stakeholder analysis
        """
        self.log_start()
        
        # Generate business analysis using AI
        result = await self.ai_service.generate_documentation(
            repo_data=self.repo_data,
            document_type="business",
            additional_context="""
            Generate comprehensive business analysis:
            
            1. SWOT Analysis:
               - Strengths: Internal positive attributes
               - Weaknesses: Internal limitations
               - Opportunities: External favorable conditions
               - Threats: External challenges
            
            2. ROI Analysis:
               - Estimated development cost
               - Potential revenue/savings
               - Break-even timeline
               - Risk factors
            
            3. Stakeholder Analysis:
               - Key stakeholders
               - Their interests and influence
               - Engagement strategy
            
            4. Market Analysis:
               - Target market
               - Competition
               - Market trends
            
            Return in JSON format matching BusinessAnalysis schema.
            """
        )
        
        # Parse result into BusinessAnalysis model
        business_analysis = BusinessAnalysis(
            swot_analysis=result.get("swot_analysis", {
                "Strengths": [],
                "Weaknesses": [],
                "Opportunities": [],
                "Threats": []
            }),
            roi_analysis=result.get("roi_analysis", {}),
            stakeholder_analysis=result.get("stakeholder_analysis", []),
            market_analysis=result.get("market_analysis", {})
        )
        
        self.log_complete()
        return business_analysis
