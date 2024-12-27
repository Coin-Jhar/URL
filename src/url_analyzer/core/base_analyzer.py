from urllib.parse import urlparse, parse_qs
import re
from typing import Dict, Any, Optional

class BaseURLAnalyzer:
    """Base class for URL analysis providing core URL parsing functionality."""
    
    SUPPORTED_SCHEMES = {'http', 'https'}
    
    def __init__(self, url: str) -> None:
        """Initialize the analyzer with a URL.
        
        Args:
            url: The URL to analyze.
            
        Raises:
            ValueError: If the URL is invalid.
        """
        if not self.is_valid_url(url):
            raise ValueError(f"Invalid URL: {url}")
            
        self.url = url
        self.parsed_url = urlparse(url)
        self.normalized_url = self._normalize_url()
        
    @staticmethod
    def is_valid_url(url: str) -> bool:
        """Check if the URL is valid and supported.
        
        Args:
            url: URL to validate.
            
        Returns:
            bool: True if URL is valid, False otherwise.
        """
        try:
            result = urlparse(url)
            return all([
                result.scheme in BaseURLAnalyzer.SUPPORTED_SCHEMES,
                result.netloc,
                '.' in result.netloc,  # Must have at least one dot
                not result.netloc.startswith('.'),  # Can't start with dot
                not result.netloc.endswith('.')  # Can't end with dot
            ])
        except Exception:
            return False
            
    def get_base_info(self) -> Dict[str, Any]:
        """Get basic information about the URL.
        
        Returns:
            dict: Dictionary containing URL components.
        """
        return {
            "scheme": self.parsed_url.scheme,
            "netloc": self.parsed_url.netloc,
            "path": self.parsed_url.path,
            "params": self.parsed_url.params,
            "query": self.parsed_url.query,
            "fragment": self.parsed_url.fragment,
            "query_params": parse_qs(self.parsed_url.query),
        }
        
    def _normalize_url(self) -> str:
        """Normalize the URL by converting to lowercase, removing default ports,
        trailing slashes, and empty query strings.
        
        Returns:
            str: Normalized URL.
        """
        # Convert scheme and netloc to lowercase
        scheme = self.parsed_url.scheme.lower()
        netloc = self.parsed_url.netloc.lower()
        
        # Remove default ports
        if f":{scheme}" in netloc:
            netloc = netloc.replace(f":{scheme}", "")
            
        # Remove trailing slash from path if it's the only path component
        path = self.parsed_url.path
        if path == "/":
            path = ""
        elif path.endswith("/"):
            path = path[:-1]
            
        # Remove empty query string
        query = self.parsed_url.query
        if not query:
            query = ""
            
        # Remove empty fragment
        fragment = self.parsed_url.fragment
        if not fragment:
            fragment = ""
            
        # Reconstruct the URL
        normalized = f"{scheme}://{netloc}{path}"
        if query:
            normalized += f"?{query}"
        if fragment:
            normalized += f"#{fragment}"
            
        return normalized
        
    def get_domain(self) -> str:
        """Extract the main domain from the URL.
        
        Returns:
            str: The main domain without subdomains.
        """
        netloc = self.parsed_url.netloc.lower()
        
        # Remove port if present
        if ':' in netloc:
            netloc = netloc.split(':')[0]
            
        parts = netloc.split('.')
        
        # Handle special cases like co.uk
        if len(parts) > 2 and parts[-2] in {'co', 'com', 'org', 'net', 'edu', 'gov'}:
            return f"{parts[-3]}.{parts[-2]}.{parts[-1]}"
            
        # Return last two parts for normal domains
        return '.'.join(parts[-2:])
