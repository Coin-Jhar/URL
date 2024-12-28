import pytest
from unittest.mock import Mock, patch
from url_analyzer.analyzers.dns_analyzer import DNSAnalyzer
from url_analyzer.utils.exceptions import DNSAnalyzerError

def test_dns_analyzer_init():
    """Test DNS analyzer initialization."""
    analyzer = DNSAnalyzer("example.com")
    assert analyzer.domain == "example.com"
    assert analyzer.resolver.nameservers == ['8.8.8.8', '8.8.4.4']

@patch('dns.resolver.Resolver')
def test_get_info(mock_resolver):
    """Test getting basic DNS information."""
    analyzer = DNSAnalyzer("example.com")
    info = analyzer.get_info()
    
    assert isinstance(info, dict)
    assert info["domain"] == "example.com"
    assert isinstance(info["nameservers"], list)
    assert info["nameservers"] == ['8.8.8.8', '8.8.4.4']

@patch('dns.resolver.Resolver')
def test_get_a_records(mock_resolver):
    """Test getting A records."""
    mock_answer = Mock()
    mock_answer.address = "93.184.216.34"
    
    resolver_instance = mock_resolver.return_value
    resolver_instance.resolve.return_value = [mock_answer]
    
    analyzer = DNSAnalyzer("example.com")
    records = analyzer.get_a_records()
    
    assert isinstance(records, list)
    assert len(records) == 1
    assert records[0] == "93.184.216.34"
    resolver_instance.resolve.assert_called_once_with("example.com", "A")

@patch('dns.resolver.Resolver')
def test_get_aaaa_records(mock_resolver):
    """Test getting AAAA records."""
    mock_answer = Mock()
    mock_answer.address = "2606:2800:220:1:248:1893:25c8:1946"
    
    resolver_instance = mock_resolver.return_value
    resolver_instance.resolve.return_value = [mock_answer]
    
    analyzer = DNSAnalyzer("example.com")
    records = analyzer.get_aaaa_records()
    
    assert isinstance(records, list)
    assert len(records) == 1
    assert records[0] == "2606:2800:220:1:248:1893:25c8:1946"
    resolver_instance.resolve.assert_called_once_with("example.com", "AAAA")

@patch('dns.resolver.Resolver')
def test_get_cname_records(mock_resolver):
    """Test getting CNAME records."""
    mock_answer = Mock()
    mock_answer.target = "target.example.com"
    
    resolver_instance = mock_resolver.return_value
    resolver_instance.resolve.return_value = [mock_answer]
    
    analyzer = DNSAnalyzer("example.com")
    records = analyzer.get_cname_records()
    
    assert isinstance(records, list)
    assert len(records) == 1
    assert records[0] == "target.example.com"
    resolver_instance.resolve.assert_called_once_with("example.com", "CNAME")

@patch('dns.resolver.Resolver')
def test_get_mx_records(mock_resolver):
    """Test getting MX records."""
    mock_answer = Mock()
    mock_answer.exchange = "mail.example.com"
    mock_answer.preference = 10
    
    resolver_instance = mock_resolver.return_value
    resolver_instance.resolve.return_value = [mock_answer]
    
    analyzer = DNSAnalyzer("example.com")
    records = analyzer.get_mx_records()
    
    assert isinstance(records, list)
    assert len(records) == 1
    assert records[0]["exchange"] == "mail.example.com"
    assert records[0]["preference"] == 10
    resolver_instance.resolve.assert_called_once_with("example.com", "MX")

@patch('dns.resolver.Resolver')
def test_get_txt_records(mock_resolver):
    """Test getting TXT records."""
    mock_answer = Mock()
    mock_answer.strings = [b"v=spf1 include:_spf.example.com ~all"]
    
    resolver_instance = mock_resolver.return_value
    resolver_instance.resolve.return_value = [mock_answer]
    
    analyzer = DNSAnalyzer("example.com")
    records = analyzer.get_txt_records()
    
    assert isinstance(records, list)
    assert len(records) == 1
    assert records[0] == "v=spf1 include:_spf.example.com ~all"
    resolver_instance.resolve.assert_called_once_with("example.com", "TXT")

@patch('dns.resolver.Resolver')
def test_get_ns_records(mock_resolver):
    """Test getting NS records."""
    mock_answer = Mock()
    mock_answer.target = "ns1.example.com"
    
    resolver_instance = mock_resolver.return_value
    resolver_instance.resolve.return_value = [mock_answer]
    
    analyzer = DNSAnalyzer("example.com")
    records = analyzer.get_ns_records()
    
    assert isinstance(records, list)
    assert len(records) == 1
    assert records[0] == "ns1.example.com"
    resolver_instance.resolve.assert_called_once_with("example.com", "NS")

@patch('dns.resolver.Resolver')
def test_get_soa_record(mock_resolver):
    """Test getting SOA record."""
    mock_answer = Mock()
    mock_answer.mname = "ns1.example.com"
    mock_answer.rname = "hostmaster.example.com"
    mock_answer.serial = 2023010100
    mock_answer.refresh = 7200
    mock_answer.retry = 3600
    mock_answer.expire = 1209600
    mock_answer.minimum = 3600
    
    resolver_instance = mock_resolver.return_value
    resolver_instance.resolve.return_value = [mock_answer]
    
    analyzer = DNSAnalyzer("example.com")
    record = analyzer.get_soa_record()
    
    assert isinstance(record, dict)
    assert record["mname"] == "ns1.example.com"
    assert record["rname"] == "hostmaster.example.com"
    assert record["serial"] == 2023010100
    assert record["refresh"] == 7200
    assert record["retry"] == 3600
    assert record["expire"] == 1209600
    assert record["minimum"] == 3600
    resolver_instance.resolve.assert_called_once_with("example.com", "SOA")

@patch('dns.resolver.Resolver')
def test_record_error_handling(mock_resolver):
    """Test error handling for DNS queries."""
    resolver_instance = mock_resolver.return_value
    resolver_instance.resolve.side_effect = Exception("DNS query failed")
    
    analyzer = DNSAnalyzer("example.com")
    records = analyzer.get_a_records()
    
    assert isinstance(records, list)
    assert len(records) == 0

@patch('dns.resolver.Resolver')
def test_analyze_method(mock_resolver):
    """Test complete DNS analysis."""
    # Mock A record
    mock_a = Mock()
    mock_a.address = "93.184.216.34"
    
    # Mock SOA record
    mock_soa = Mock()
    mock_soa.mname = "ns1.example.com"
    mock_soa.rname = "hostmaster.example.com"
    mock_soa.serial = 2023010100
    mock_soa.refresh = 7200
    mock_soa.retry = 3600
    mock_soa.expire = 1209600
    mock_soa.minimum = 3600
    
    def mock_resolve(domain, record_type):
        if record_type == "A":
            return [mock_a]
        elif record_type == "SOA":
            return [mock_soa]
        raise Exception(f"No {record_type} record")
    
    resolver_instance = mock_resolver.return_value
    resolver_instance.resolve.side_effect = mock_resolve
    
    analyzer = DNSAnalyzer("example.com")
    result = analyzer.analyze()
    
    assert isinstance(result, dict)
    assert "info" in result
    assert "records" in result
    assert result["info"]["domain"] == "example.com"
    assert result["records"]["a_records"] == ["93.184.216.34"]
    assert result["records"]["soa_record"]["mname"] == "ns1.example.com"
