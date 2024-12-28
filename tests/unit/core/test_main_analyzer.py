import pytest
from unittest.mock import Mock, patch
from url_analyzer.core.main_analyzer import MainAnalyzer

@pytest.fixture
def sample_url():
    return "https://example.com/path?param=value"

@pytest.fixture
def mock_url_analysis():
    return {
        "url": "https://example.com/path?param=value",
        "normalized_url": "https://example.com/path?param=value",
        "components": {
            "scheme": "https",
            "netloc": "example.com",
            "path": "/path",
            "params": "",
            "query": "param=value",
            "fragment": "",
            "query_params": {"param": ["value"]}
        },
        "domain": "example.com"
    }

@pytest.fixture
def mock_dns_analysis():
    return {
        "info": {
            "domain": "example.com",
            "nameservers": ["8.8.8.8", "8.8.4.4"]
        },
        "records": {
            "a_records": ["93.184.216.34"],
            "aaaa_records": ["2606:2800:220:1:248:1893:25c8:1946"],
            "cname_records": [],
            "mx_records": [],
            "txt_records": ["v=spf1 -all"],
            "ns_records": ["ns1.example.com"],
            "soa_record": {
                "mname": "ns1.example.com"
            }
        }
    }

def test_main_analyzer_init(sample_url):
    """Test MainAnalyzer initialization."""
    analyzer = MainAnalyzer(sample_url)
    assert analyzer.url == sample_url
    assert analyzer.url_analyzer is not None
    assert analyzer.dns_analyzer is not None

@patch('url_analyzer.core.url_analyzer.URLAnalyzer.analyze')
@patch('url_analyzer.analyzers.dns_analyzer.DNSAnalyzer.analyze')
def test_main_analyzer_analyze(mock_dns_analyze, mock_url_analyze, 
                             sample_url, mock_url_analysis, mock_dns_analysis):
    """Test complete analysis with mocked components."""
    mock_url_analyze.return_value = mock_url_analysis
    mock_dns_analyze.return_value = mock_dns_analysis
    
    analyzer = MainAnalyzer(sample_url)
    result = analyzer.analyze()
    
    assert isinstance(result, dict)
    assert "info" in result
    assert "url_analysis" in result
    assert "dns_analysis" in result
    
    # Verify URL analysis
    assert result["url_analysis"] == mock_url_analysis
    
    # Verify DNS analysis
    assert result["dns_analysis"] == mock_dns_analysis
    
    # Verify basic info
    assert result["info"]["url"] == sample_url
    assert result["info"]["domain"] == "example.com"
    assert "normalized_url" in result["info"]

def test_get_info(sample_url):
    """Test getting basic information."""
    analyzer = MainAnalyzer(sample_url)
    info = analyzer.get_info()
    
    assert isinstance(info, dict)
    assert info["url"] == sample_url
    assert "domain" in info
    assert "normalized_url" in info
