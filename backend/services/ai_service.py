"""
AI service for generating documentation using Claude or GPT
"""
import json
from typing import Dict, Any, Optional
from abc import ABC, abstractmethod
from core.config import settings
from core.logger import logger
from core.exceptions import AIServiceException


class AIProvider(ABC):
    """Abstract base class for AI providers"""
    
    @abstractmethod
    async def generate_completion(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        """Generate AI completion"""
        pass


class AnthropicProvider(AIProvider):
    """Anthropic Claude AI provider"""
    
    def __init__(self, api_key: str):
        try:
            from anthropic import AsyncAnthropic
            self.client = AsyncAnthropic(api_key=api_key)
            self.model = settings.ANTHROPIC_MODEL
        except ImportError:
            raise AIServiceException("anthropic package not installed. Install with: pip install anthropic")
    
    async def generate_completion(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        """
        Generate completion using Claude
        
        Args:
            prompt: User prompt
            system_prompt: System prompt for context
            
        Returns:
            Generated text
        """
        try:
            messages = [{"role": "user", "content": prompt}]
            
            response = await self.client.messages.create(
                model=self.model,
                max_tokens=settings.AI_MAX_TOKENS,
                temperature=settings.AI_TEMPERATURE,
                system=system_prompt or "You are a helpful AI assistant specialized in software documentation and analysis.",
                messages=messages
            )
            
            return response.content[0].text
        except Exception as e:
            logger.error(f"Anthropic API error: {e}")
            raise AIServiceException(f"Failed to generate completion with Claude: {str(e)}")


class OpenAIProvider(AIProvider):
    """OpenAI GPT provider"""
    
    def __init__(self, api_key: str):
        try:
            from openai import AsyncOpenAI
            self.client = AsyncOpenAI(api_key=api_key)
            self.model = settings.OPENAI_MODEL
        except ImportError:
            raise AIServiceException("openai package not installed. Install with: pip install openai")


class PerplexityProvider(AIProvider):
    """Perplexity AI provider"""
    
    def __init__(self, api_key: str):
        try:
            from openai import AsyncOpenAI
            self.client = AsyncOpenAI(
                api_key=api_key,
                base_url="https://api.perplexity.ai"
            )
            self.model = settings.PERPLEXITY_MODEL
        except ImportError:
            raise AIServiceException("openai package not installed. Install with: pip install openai")
    
    async def generate_completion(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        """
        Generate completion using GPT
        
        Args:
            prompt: User prompt
            system_prompt: System prompt for context
            
        Returns:
            Generated text
        """
        try:
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": prompt})
            
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=settings.AI_MAX_TOKENS,
                temperature=settings.AI_TEMPERATURE
            )
            
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"OpenAI API error: {e}")
            raise AIServiceException(f"Failed to generate completion with GPT: {str(e)}")


class AIService:
    """Main AI service class"""
    
    def __init__(self, provider: str = "anthropic"):
        """
        Initialize AI service
        
        Args:
            provider: AI provider name ("anthropic", "openai", or "perplexity")
        """
        self.provider_name = provider
        
        if provider == "anthropic":
            if not settings.ANTHROPIC_API_KEY:
                raise AIServiceException("ANTHROPIC_API_KEY not configured")
            self.provider = AnthropicProvider(settings.ANTHROPIC_API_KEY)
        elif provider == "openai":
            if not settings.OPENAI_API_KEY:
                raise AIServiceException("OPENAI_API_KEY not configured")
            self.provider = OpenAIProvider(settings.OPENAI_API_KEY)
        elif provider == "perplexity":
            if not settings.PERPLEXITY_API_KEY:
                raise AIServiceException("PERPLEXITY_API_KEY not configured")
            self.provider = PerplexityProvider(settings.PERPLEXITY_API_KEY)
        else:
            raise AIServiceException(f"Unsupported AI provider: {provider}")
        
        logger.info(f"AI Service initialized with provider: {provider}")
    
    async def generate_documentation(
        self,
        repo_data: Dict[str, Any],
        document_type: str,
        additional_context: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Generate documentation based on repository data
        
        Args:
            repo_data: Repository analysis data
            document_type: Type of document to generate
            additional_context: Additional context for generation
            
        Returns:
            Generated documentation as dictionary
        """
        logger.info(f"Generating {document_type} documentation")
        
        # Prepare context from repo data
        context = self._prepare_context(repo_data)
        
        # Get appropriate prompt template
        system_prompt, user_prompt = self._get_prompt_template(document_type, context, additional_context)
        
        try:
            # Generate completion
            response = await self.provider.generate_completion(user_prompt, system_prompt)
            
            # Parse response (assuming JSON format)
            try:
                result = json.loads(response)
            except json.JSONDecodeError:
                # If not JSON, wrap in result object
                result = {"content": response, "raw": True}
            
            logger.info(f"Successfully generated {document_type} documentation")
            return result
            
        except Exception as e:
            logger.error(f"Failed to generate documentation: {e}")
            raise AIServiceException(f"Failed to generate documentation: {str(e)}")
    
    def _prepare_context(self, repo_data: Dict[str, Any]) -> str:
        """Prepare context string from repository data"""
        repo_info = repo_data.get("repository", {})
        
        context = f"""
Repository Information:
- Name: {repo_info.get('name', 'Unknown')}
- Description: {repo_info.get('description', 'No description')}
- Language: {repo_info.get('language', 'Unknown')}
- Stars: {repo_info.get('stargazers_count', 0)}
- Forks: {repo_info.get('forks_count', 0)}

Languages Used:
{json.dumps(repo_data.get('languages', {}), indent=2)}

File Structure:
Total Files: {repo_data['statistics']['total_files']}
Total Directories: {repo_data['statistics']['total_dirs']}

README Content:
{repo_data.get('readme', 'No README available')[:2000]}

Recent Activity:
Total Commits: {repo_data['statistics']['total_commits']}
Contributors: {repo_data['statistics']['total_contributors']}
"""
        return context
    
    def _get_prompt_template(
        self,
        document_type: str,
        context: str,
        additional_context: Optional[str]
    ) -> tuple[str, str]:
        """Get prompt template for specific document type"""
        
        base_system = "You are an expert software architect and technical writer. Analyze the provided repository data and generate comprehensive, professional documentation."
        
        prompts = {
            "scope": (
                base_system,
                f"""{context}

Generate a comprehensive Project Scope Document in JSON format with the following structure:
{{
  "project_overview": "detailed overview",
  "objectives": ["objective1", "objective2"],
  "scope_in": ["what's included"],
  "scope_out": ["what's excluded"],
  "assumptions": ["assumption1"],
  "constraints": ["constraint1"],
  "deliverables": ["deliverable1"]
}}

{additional_context or ''}
"""
            ),
            "uml": (
                base_system,
                f"""{context}

Generate UML diagrams in JSON format with PlantUML syntax:
{{
  "use_case_diagram": "@startuml\\n...\\n@enduml",
  "class_diagram": "@startuml\\n...\\n@enduml",
  "sequence_diagrams": [{{"name": "...", "diagram": "@startuml\\n...\\n@enduml"}}],
  "activity_diagrams": [{{"name": "...", "diagram": "@startuml\\n...\\n@enduml"}}]
}}

{additional_context or ''}
"""
            ),
            "architecture": (
                base_system,
                f"""{context}

Generate system architecture documentation in JSON format:
{{
  "system_architecture": "detailed description",
  "component_diagram": "@startuml\\n...\\n@enduml",
  "deployment_diagram": "@startuml\\n...\\n@enduml",
  "erd_diagram": "@startuml\\n...\\n@enduml",
  "api_documentation": {{}},
  "technology_stack": {{
    "frontend": [],
    "backend": [],
    "database": [],
    "infrastructure": []
  }}
}}

{additional_context or ''}
"""
            )
        }
        
        return prompts.get(document_type, (base_system, f"{context}\n\nGenerate documentation for: {document_type}"))
    
    async def analyze_code_quality(self, repo_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze code quality based on repository data
        
        Args:
            repo_data: Repository analysis data
            
        Returns:
            Code quality analysis
        """
        logger.info("Analyzing code quality")
        
        context = self._prepare_context(repo_data)
        
        system_prompt = "You are a code quality expert. Analyze the repository and provide detailed quality metrics."
        
        user_prompt = f"""{context}

Analyze the code quality and provide results in JSON format:
{{
  "code_quality_score": 85.5,
  "code_metrics": {{
    "maintainability_index": 75,
    "cyclomatic_complexity": "medium",
    "code_coverage": "unknown"
  }},
  "technical_debt": {{
    "estimated_days": 15,
    "priority_issues": []
  }},
  "security_issues": [],
  "performance_analysis": {{}},
  "recommendations": []
}}
"""
        
        try:
            response = await self.provider.generate_completion(user_prompt, system_prompt)
            result = json.loads(response)
            logger.info("Code quality analysis completed")
            return result
        except Exception as e:
            logger.error(f"Failed to analyze code quality: {e}")
            raise AIServiceException(f"Failed to analyze code quality: {str(e)}")
