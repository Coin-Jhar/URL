import pytest
from unittest.mock import patch, Mock
from url_analyzer.cli.main import main, format_url_output, format_dns_output, format_full_output

@pytest.fixture
def mock_url_analysis():
    return {
        "components": {
            "scheme": "https",
            "netloc": "example.com",
            "path": "/path",
            "params": "",
            "query": "param=value",
            "fragment": "",
            "query_params": {"param": ["value"]}
        }
    }

@pytest.fixture
def mock_dns_analysis():
    return {
        "records": {
            "a_records": ["93.184.216.34"],
            "aaaa_records": ["2606:2800:220:1:248:1893:25c8:1946"],
            "cname_records": [],
            "mx_records": [{"preference": 10, "exchange": "mail.example.com"}],
            "txt_records": ["v=spf1 -all"],
            "ns_records": ["ns1.example.com"],
            "soa_record": {
                "mname": "ns1.example.com",
                "rname": "admin.example.com"
            }
        }
    }

@pytest.fixture
def mock_full_analysis():
    return {
        "info": {
            "url": "https://example.com/path?param=value",
            "domain": "example.com",
            "normalized_url": "https://example.com/path?param=value"
        },
        "url_analysis": {
            "components": {
                "scheme": "https",
                "netloc": "example.com",
                "path": "/path",
                "params": "",
                "query": "param=value",
                "fragment": "",
                "query_params": {"param": ["value"]}
            }
        },
        "dns_analysis": {
            "records": {
                "a_records": ["93.184.216.34"],
                "aaaa_records": [],
                "cname_records": [],
                "mx_records": [],
                "txt_records": [],
                "ns_records": [],
                "soa_record": {}
            }
        }
    }

def test_format_url_output(mock_url_analysis):
    """Test URL output formatting."""
    # Test text format
    text_output = format_url_output(mock_url_analysis)
    assert "URL Analysis:" in text_output
    assert "Scheme: https" in text_output
    assert "Netloc: example.com" in text_output
    
    # Test JSON format
    json_output = format_url_output(mock_url_analysis, text_format=False)
    assert '"scheme": "https"' in json_output
    assert '"netloc": "example.com"' in json_output

def test_format_dns_output(mock_dns_analysis):
    """Test DNS output formatting."""
    # Test text format
    text_output = format_dns_output(mock_dns_analysis)
    assert "DNS Records:" in text_output
    assert "A Records:" in text_output
    assert "93.184.216.34" in text_output
    
    # Test JSON format
    json_output = format_dns_output(mock_dns_analysis, text_format=False)
    assert '"a_records":' in json_output
    assert '"93.184.216.34"' in json_output

def test_format_full_output(mock_full_analysis):
    """Test full analysis output formatting."""
    # Test text format
    text_output = format_full_output(mock_full_analysis)
    assert "Basic Information:" in text_output
    assert "URL Analysis:" in text_output
    assert "DNS Records:" in text_output
    
    # Test JSON format
    json_output = format_full_output(mock_full_analysis, text_format=False)
    assert '"info":' in json_output
    assert '"url_analysis":' in json_output
    assert '"dns_analysis":' in json_output

@patch('sys.argv', ['url-analyzer', 'https://example.com'])
@patch('url_analyzer.core.url_analyzer.URLAnalyzer.analyze')
def test_cli_url_mode(mock_analyze, mock_url_analysis, capsys):
    """Test CLI in URL mode."""
    mock_analyze.return_value = mock_url_analysis
    main()
    captured = capsys.readouterr()
    assert "URL Analysis:" in captured.out
    assert "Scheme: https" in captured.out

@patch('sys.argv', ['url-analyzer', 'https://example.com', '--mode', 'dns'])
@patch('url_analyzer.analyzers.dns_analyzer.DNSAnalyzer.analyze')
def test_cli_dns_mode(mock_analyze, mock_dns_analysis, capsys):
    """Test CLI in DNS mode."""
    mock_analyze.return_value = mock_dns_analysis
    main()
    captured = capsys.readouterr()
    assert "DNS Records:" in captured.out
    assert "A Records:" in captured.out

@patch('sys.argv', ['url-analyzer', 'https://example.com', '--mode', 'full'])
@patch('url_analyzer.core.main_analyzer.MainAnalyzer.analyze')
def test_cli_full_mode(mock_analyze, mock_full_analysis, capsys):
    """Test CLI in full mode."""
    mock_analyze.return_value = mock_full_analysis
    main()
    captured = capsys.readouterr()
    assert "Basic Information:" in captured.out
    assert "URL Analysis:" in captured.out
    assert "DNS Records:" in captured.out

@patch('sys.argv', ['url-analyzer', 'invalid-url'])
def test_cli_error_handling(capsys):
    """Test CLI error handling."""
    with pytest.raises(SystemExit):
        main()
    captured = capsys.readouterr()
    assert "Error:" in captured.out
