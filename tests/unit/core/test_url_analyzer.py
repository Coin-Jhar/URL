import pytest
from urllib.parse import ParseResult
from url_analyzer.core.url_analyzer import URLAnalyzer
from url_analyzer.utils.exceptions import InvalidURLError

def test_url_analyzer_initialization():
    """Test if URLAnalyzer initializes correctly with a valid URL."""
    url = "https://example.com/path?param=value"
    analyzer = URLAnalyzer(url)
    assert analyzer.url == url
    assert isinstance(analyzer.parsed_url, ParseResult)

def test_url_analyzer_invalid_url():
    """Test if URLAnalyzer raises ValueError for invalid URLs."""
    with pytest.raises(InvalidURLError):
        URLAnalyzer("not-a-valid-url")

def test_get_info():
    """Test if get_info returns correct URL components."""
    url = "https://example.com:8080/path?param=value#fragment"
    analyzer = URLAnalyzer(url)
    base_info = analyzer.get_info()
    
    assert base_info["scheme"] == "https"
    assert base_info["netloc"] == "example.com:8080"
    assert base_info["path"] == "/path"
    assert base_info["params"] == ""
    assert base_info["query"] == "param=value"
    assert base_info["fragment"] == "fragment"
    assert isinstance(base_info["query_params"], dict)
    assert base_info["query_params"]["param"] == ["value"]

def test_normalize_url():
    """Test URL normalization."""
    test_cases = [
        ("HTTP://ExAmPlE.CoM", "http://example.com"),
        ("http://example.com/", "http://example.com"),
        ("http://example.com/path/", "http://example.com/path"),
        ("http://example.com/?", "http://example.com"),
    ]
    
    for input_url, expected_url in test_cases:
        analyzer = URLAnalyzer(input_url)
        assert analyzer.normalized_url == expected_url

def test_is_valid_url():
    """Test URL validation."""
    valid_urls = [
        "https://example.com",
        "http://example.co.uk/path",
        "https://sub.example.com:8080",
    ]
    
    invalid_urls = [
        "not-a-url",
        "http://",
        "https://.com",
        "ftp://example.com",  # Assuming we only support http/https
    ]
    
    for url in valid_urls:
        assert URLAnalyzer.is_valid_url(url) is True
        
    for url in invalid_urls:
        assert URLAnalyzer.is_valid_url(url) is False

def test_get_domain():
    """Test domain extraction."""
    test_cases = [
        ("https://example.com/path", "example.com"),
        ("https://sub.example.co.uk/path", "example.co.uk"),
        ("http://sub1.sub2.example.com", "example.com"),
    ]
    
    for url, expected_domain in test_cases:
        analyzer = URLAnalyzer(url)
        assert analyzer.get_domain() == expected_domain

def test_analyze():
    """Test complete URL analysis."""
    url = "https://example.com/path?param=value"
    analyzer = URLAnalyzer(url)
    result = analyzer.analyze()
    
    assert isinstance(result, dict)
    assert result["url"] == url
    assert result["normalized_url"] == url.lower()
    assert isinstance(result["components"], dict)
    assert result["domain"] == "example.com"
