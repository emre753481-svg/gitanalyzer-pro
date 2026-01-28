"""
Architecture analyzer - Generates architecture documentation
"""
from typing import Dict, Any
from .base import BaseAnalyzer
from models.schemas import Architecture


class ArchitectureAnalyzer(BaseAnalyzer):
    """Analyzer for generating architecture documentation"""
    
    async def analyze(self) -> Architecture:
        """
        Generate architecture documentation
        
        Returns:
            Architecture with system design, diagrams, and tech stack
        """
        self.log_start()
        
        # Generate architecture documentation using AI
        result = await self.ai_service.generate_documentation(
            repo_data=self.repo_data,
            document_type="architecture",
            additional_context="""
            Generate comprehensive architecture documentation:
            
            1. System Architecture Description:
               - High-level architecture overview
               - Key components and their interactions
               - Design patterns used
               - Architectural decisions and rationale
            
            2. Component Diagram (PlantUML):
               - Show major components/modules
               - Dependencies between components
               - External systems/services
            
            3. Deployment Diagram (PlantUML):
               - Infrastructure layout
               - Servers, databases, services
               - Network topology
            
            4. ERD Diagram (PlantUML):
               - Database entities
               - Relationships
               - Key fields
            
            5. API Documentation:
               - Endpoints
               - Request/response formats
               - Authentication
            
            6. Technology Stack:
               - Frontend technologies
               - Backend technologies
               - Databases
               - Infrastructure & DevOps
            
            Return in JSON format matching Architecture schema.
            """
        )
        
        # Parse result into Architecture model
        architecture = Architecture(
            system_architecture=result.get("system_architecture", ""),
            component_diagram=result.get("component_diagram", "@startuml\n@enduml"),
            deployment_diagram=result.get("deployment_diagram", "@startuml\n@enduml"),
            erd_diagram=result.get("erd_diagram", "@startuml\n@enduml"),
            api_documentation=result.get("api_documentation", {}),
            technology_stack=result.get("technology_stack", {
                "frontend": [],
                "backend": [],
                "database": [],
                "infrastructure": []
            })
        )
        
        self.log_complete()
        return architecture
