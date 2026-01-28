"""
UML analyzer - Generates UML diagrams
"""
from typing import Dict, Any, List
from .base import BaseAnalyzer
from models.schemas import UMLDiagrams


class UMLAnalyzer(BaseAnalyzer):
    """Analyzer for generating UML diagrams"""
    
    async def analyze(self) -> UMLDiagrams:
        """
        Generate UML diagrams
        
        Returns:
            UMLDiagrams with various UML diagrams
        """
        self.log_start()
        
        # Generate UML diagrams using AI
        result = await self.ai_service.generate_documentation(
            repo_data=self.repo_data,
            document_type="uml",
            additional_context="""
            Generate comprehensive UML diagrams in PlantUML syntax:
            1. Use Case Diagram - showing actors and use cases
            2. Class Diagram - showing main classes and relationships
            3. Sequence Diagrams - showing key interactions
            4. Activity Diagrams - showing workflows
            
            Use proper PlantUML syntax with @startuml and @enduml tags.
            """
        )
        
        # Parse result into UMLDiagrams model
        uml_diagrams = UMLDiagrams(
            use_case_diagram=result.get("use_case_diagram", "@startuml\n@enduml"),
            class_diagram=result.get("class_diagram", "@startuml\n@enduml"),
            sequence_diagrams=result.get("sequence_diagrams", []),
            activity_diagrams=result.get("activity_diagrams", [])
        )
        
        self.log_complete()
        return uml_diagrams
