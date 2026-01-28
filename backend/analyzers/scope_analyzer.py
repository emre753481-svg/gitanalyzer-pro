"""
Scope analyzer - Generates project scope document
"""
from typing import Dict, Any
from .base import BaseAnalyzer
from models.schemas import ScopeDocument


class ScopeAnalyzer(BaseAnalyzer):
    """Analyzer for generating project scope document"""
    
    async def analyze(self) -> ScopeDocument:
        """
        Generate project scope document
        
        Returns:
            ScopeDocument with project scope details
        """
        self.log_start()
        
        # Generate scope document using AI
        result = await self.ai_service.generate_documentation(
            repo_data=self.repo_data,
            document_type="scope",
            additional_context="""
            Focus on:
            - Clear project objectives and goals
            - Detailed scope boundaries (in/out of scope)
            - Realistic assumptions and constraints
            - Concrete deliverables
            
            Make it professional and actionable.
            """
        )
        
        # Parse result into ScopeDocument model
        scope_doc = ScopeDocument(
            project_overview=result.get("project_overview", ""),
            objectives=result.get("objectives", []),
            scope_in=result.get("scope_in", []),
            scope_out=result.get("scope_out", []),
            assumptions=result.get("assumptions", []),
            constraints=result.get("constraints", []),
            deliverables=result.get("deliverables", [])
        )
        
        self.log_complete()
        return scope_doc
