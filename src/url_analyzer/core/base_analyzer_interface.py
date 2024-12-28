from abc import ABC, abstractmethod
from typing import Dict, Any

class BaseAnalyzer(ABC):
    """Base interface for all analyzers."""
    
    @abstractmethod
    def analyze(self) -> Dict[str, Any]:
        """Perform the analysis.
        
        Returns:
            Dict containing analysis results
        """
        pass
    
    @abstractmethod
    def get_info(self) -> Dict[str, Any]:
        """Get basic information.
        
        Returns:
            Dict containing basic information
        """
        pass
