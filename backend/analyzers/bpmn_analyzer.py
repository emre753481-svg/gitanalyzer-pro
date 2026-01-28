"""
BPMN analyzer - Generates BPMN diagrams
"""
from typing import Dict, Any, List
from .base import BaseAnalyzer
from models.schemas import BPMNDiagrams


class BPMNAnalyzer(BaseAnalyzer):
    """Analyzer for generating BPMN business process diagrams"""
    
    async def analyze(self) -> BPMNDiagrams:
        """
        Generate BPMN diagrams
        
        Returns:
            BPMNDiagrams with business process flows
        """
        self.log_start()
        
        # Generate BPMN diagrams using AI
        result = await self.ai_service.generate_documentation(
            repo_data=self.repo_data,
            document_type="bpmn",
            additional_context="""
            Generate BPMN (Business Process Model and Notation) diagrams:
            1. Identify key business processes in the application
            2. Map out process flows with start/end events, tasks, gateways
            3. Show swimlanes for different actors/systems
            
            Return in JSON format:
            {
              "business_processes": [
                {
                  "name": "Process Name",
                  "description": "Process description",
                  "steps": ["step1", "step2"]
                }
              ],
              "process_flows": ["BPMN notation or PlantUML"]
            }
            """
        )
        
        # Parse result into BPMNDiagrams model
        bpmn_diagrams = BPMNDiagrams(
            business_processes=result.get("business_processes", []),
            process_flows=result.get("process_flows", [])
        )
        
        self.log_complete()
        return bpmn_diagrams
