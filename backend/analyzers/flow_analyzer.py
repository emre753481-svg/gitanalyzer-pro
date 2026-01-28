"""
Flow analyzer - Generates flow diagrams (user journey, data flow)
"""
from typing import Dict, Any, List
from .base import BaseAnalyzer
from models.schemas import FlowDiagrams


class FlowAnalyzer(BaseAnalyzer):
    """Analyzer for generating flow diagrams"""
    
    async def analyze(self) -> FlowDiagrams:
        """
        Generate flow diagrams
        
        Returns:
            FlowDiagrams with user journey and data flow diagrams
        """
        self.log_start()
        
        # Generate flow diagrams using AI
        result = await self.ai_service.generate_documentation(
            repo_data=self.repo_data,
            document_type="flow",
            additional_context="""
            Generate flow diagrams:
            1. User Journey Maps - showing user interactions and touchpoints
            2. Data Flow Diagrams - showing how data moves through the system
            3. System Flow - overall system interaction flow
            
            Return in JSON format:
            {
              "user_journey_maps": [
                {
                  "persona": "User Type",
                  "journey": "Description",
                  "touchpoints": ["point1", "point2"],
                  "pain_points": ["pain1"],
                  "opportunities": ["opp1"]
                }
              ],
              "data_flow_diagrams": ["DFD notation or description"],
              "system_flow": "PlantUML or Mermaid diagram"
            }
            """
        )
        
        # Parse result into FlowDiagrams model
        flow_diagrams = FlowDiagrams(
            user_journey_maps=result.get("user_journey_maps", []),
            data_flow_diagrams=result.get("data_flow_diagrams", []),
            system_flow=result.get("system_flow", "")
        )
        
        self.log_complete()
        return flow_diagrams
