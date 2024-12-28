from urllib.parse import urlparse, parse_qs
from typing import Dict, Any
from url_analyzer.core.base_analyzer_interface import BaseAnalyzer
from url_analyzer.utils.exceptions import InvalidURLError

class URLAnalyzer(BaseAnalyzer):
    """URL component analyzer."""
    
    SUPPORTED_SCHEMES = {'http', 'https'}
    
    def __init__(self, url: str):
        if not self.is_valid_url(url):
            raise InvalidURLError(f"Invalid URL: {url}")
            
        self.url = url
        self.parsed_url = urlparse(url)
        self.normalized_url = self._normalize_url()
    
    def get_info(self) -> Dict[str, Any]:
        """Get basic URL information."""
        return {
            "scheme": self.parsed_url.scheme,
            "netloc": self.parsed_url.netloc,
            "path": self.parsed_url.path,
            "params": self.parsed_url.params,
            "query": self.parsed_url.query,
            "fragment": self.parsed_url.fragment,
            "query_params": parse_qs(self.parsed_url.query),
        }
    
    def analyze(self) -> Dict[str, Any]:
        """Perform complete URL analysis."""
        return {
            "url": self.url,
            "normalized_url": self.normalized_url,
            "components": self.get_info(),
            "domain": self.get_domain()
        }
    
    @staticmethod
    def is_valid_url(url: str) -> bool:
        try:
            result = urlparse(url)
            return all([
                result.scheme in URLAnalyzer.SUPPORTED_SCHEMES,
                result.netloc,
                '.' in result.netloc,
                not result.netloc.startswith('.'),
                not result.netloc.endswith('.')
            ])
        except Exception:
            return False
            
    def _normalize_url(self) -> str:
        """Normalize the URL."""
        scheme = self.parsed_url.scheme.lower()
        netloc = self.parsed_url.netloc.lower()
        
        if f":{scheme}" in netloc:
            netloc = netloc.replace(f":{scheme}", "")
            
        path = self.parsed_url.path
        if path == "/":
            path = ""
        elif path.endswith("/"):
            path = path[:-1]
            
        query = self.parsed_url.query
        if not query:
            query = ""
            
        fragment = self.parsed_url.fragment
        if not fragment:
            fragment = ""
            
        normalized = f"{scheme}://{netloc}{path}"
        if query:
            normalized += f"?{query}"
        if fragment:
            normalized += f"#{fragment}"
            
        return normalized
        
    def get_domain(self) -> str:
        """Extract the main domain."""
        netloc = self.parsed_url.netloc.lower()
        
        if ':' in netloc:
            netloc = netloc.split(':')[0]
            
        parts = netloc.split('.')
        
        if len(parts) > 2 and parts[-2] in {'co', 'com', 'org', 'net', 'edu', 'gov'}:
            return f"{parts[-3]}.{parts[-2]}.{parts[-1]}"
            
        return '.'.join(parts[-2:])
