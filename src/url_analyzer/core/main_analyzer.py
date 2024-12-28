from typing import Dict, Any
from urllib.parse import urlparse
from url_analyzer.core.base_analyzer_interface import BaseAnalyzer
from url_analyzer.core.url_analyzer import URLAnalyzer
from url_analyzer.analyzers.dns_analyzer import DNSAnalyzer

class MainAnalyzer(BaseAnalyzer):
    """Main analyzer that combines URL and DNS analysis."""
    
    def __init__(self, url: str):
        self.url = url
        self.url_analyzer = URLAnalyzer(url)
        # Extract domain from URL for DNS analysis
        self.dns_analyzer = DNSAnalyzer(urlparse(url).netloc)
    
    def get_info(self) -> Dict[str, Any]:
        """Get basic information from all analyzers."""
        return {
            "url": self.url,
            "domain": self.url_analyzer.get_domain(),
            "normalized_url": self.url_analyzer.normalized_url
        }
    
    def analyze(self) -> Dict[str, Any]:
        """Perform complete analysis using all analyzers."""
        return {
            "info": self.get_info(),
            "url_analysis": self.url_analyzer.analyze(),
            "dns_analysis": self.dns_analyzer.analyze()
        }
