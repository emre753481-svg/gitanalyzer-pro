"""
Base analyzer class
"""
from abc import ABC, abstractmethod
from typing import Dict, Any
from core.logger import logger


class BaseAnalyzer(ABC):
    """Base class for all analyzers"""
    
    def __init__(self, ai_service, repo_data: Dict[str, Any]):
        """
        Initialize analyzer
        
        Args:
            ai_service: AI service instance
            repo_data: Repository data from GitHub
        """
        self.ai_service = ai_service
        self.repo_data = repo_data
        self.analyzer_name = self.__class__.__name__
    
    @abstractmethod
    async def analyze(self) -> Dict[str, Any]:
        """
        Perform analysis
        
        Returns:
            Analysis results
        """
        pass
    
    def log_start(self):
        """Log analysis start"""
        logger.info(f"Starting {self.analyzer_name} analysis")
    
    def log_complete(self):
        """Log analysis completion"""
        logger.info(f"Completed {self.analyzer_name} analysis")
