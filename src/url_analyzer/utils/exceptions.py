class URLAnalyzerError(Exception):
    """Base exception class for URL Analyzer."""
    pass

class InvalidURLError(URLAnalyzerError):
    """Raised when a URL is invalid."""
    pass

class DNSAnalyzerError(URLAnalyzerError):
    """Raised when there's an error in DNS analysis."""
    pass

class ConnectionError(URLAnalyzerError):
    """Raised when there's an error connecting to the URL."""
    pass

class SSLError(URLAnalyzerError):
    """Raised when there's an SSL/TLS-related error."""
    pass

class TimeoutError(URLAnalyzerError):
    """Raised when a request times out."""
    pass

class ParsingError(URLAnalyzerError):
    """Raised when there's an error parsing URL components or content."""
    pass
