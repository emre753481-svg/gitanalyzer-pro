"""
Requirements analyzer - Generates requirements documentation
"""
from typing import Dict, Any, List
from .base import BaseAnalyzer
from models.schemas import Requirements


class RequirementsAnalyzer(BaseAnalyzer):
    """Analyzer for generating requirements documentation"""
    
    async def analyze(self) -> Requirements:
        """
        Generate requirements documentation
        
        Returns:
            Requirements with functional, non-functional requirements and user stories
        """
        self.log_start()
        
        # Generate requirements using AI
        result = await self.ai_service.generate_documentation(
            repo_data=self.repo_data,
            document_type="requirements",
            additional_context="""
            Generate comprehensive requirements documentation:
            
            1. Functional Requirements:
               - What the system must do
               - Specific features and capabilities
               - Input/output specifications
               Format: [{"id": "FR-001", "title": "...", "description": "...", "priority": "high/medium/low"}]
            
            2. Non-Functional Requirements:
               - Performance, security, usability
               - Scalability, reliability
               - Compliance requirements
               Format: [{"id": "NFR-001", "category": "performance", "description": "...", "metric": "..."}]
            
            3. User Stories:
               - As a [role], I want to [action], so that [benefit]
               Format: [{"id": "US-001", "role": "user", "action": "...", "benefit": "...", "priority": "high"}]
            
            4. Acceptance Criteria:
               - Testable conditions for each story
               Format: [{"story_id": "US-001", "criteria": "...", "test_case": "..."}]
            
            Return in JSON format matching Requirements schema.
            """
        )
        
        # Parse result into Requirements model
        requirements = Requirements(
            functional_requirements=result.get("functional_requirements", []),
            non_functional_requirements=result.get("non_functional_requirements", []),
            user_stories=result.get("user_stories", []),
            acceptance_criteria=result.get("acceptance_criteria", [])
        )
        
        self.log_complete()
        return requirements
