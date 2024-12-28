import argparse
import json
from url_analyzer.core.main_analyzer import MainAnalyzer
from url_analyzer.core.url_analyzer import URLAnalyzer
from url_analyzer.analyzers.dns_analyzer import DNSAnalyzer
from urllib.parse import urlparse
from url_analyzer.utils.exceptions import URLAnalyzerError, DNSAnalyzerError

def format_url_output(results: dict, text_format: bool = True) -> str:
    """Format URL analysis results."""
    if not text_format:
        return json.dumps(results, indent=2)
    
    output = []
    output.append("\nURL Analysis:")
    output.append("-" * 50)
    
    components = results["components"]
    for key, value in components.items():
        output.append(f"{key.replace('_', ' ').title()}: {value}")
    
    return "\n".join(output)

def format_dns_output(results: dict, text_format: bool = True) -> str:
    """Format DNS analysis results."""
    if not text_format:
        return json.dumps(results, indent=2)
    
    output = []
    output.append("\nDNS Records:")
    output.append("-" * 50)
    
    records = results["records"]
    
    if records["a_records"]:
        output.append("\nA Records:")
        for record in records["a_records"]:
            output.append(f"  {record}")
    
    if records["aaaa_records"]:
        output.append("\nAAAA Records:")
        for record in records["aaaa_records"]:
            output.append(f"  {record}")
    
    if records["cname_records"]:
        output.append("\nCNAME Records:")
        for record in records["cname_records"]:
            output.append(f"  {record}")
    
    if records["mx_records"]:
        output.append("\nMX Records:")
        for record in records["mx_records"]:
            output.append(f"  Priority: {record['preference']}")
            output.append(f"  Exchange: {record['exchange']}")
    
    if records["txt_records"]:
        output.append("\nTXT Records:")
        for record in records["txt_records"]:
            output.append(f"  {record}")
    
    if records["ns_records"]:
        output.append("\nNS Records:")
        for record in records["ns_records"]:
            output.append(f"  {record}")
    
    if records["soa_record"]:
        output.append("\nSOA Record:")
        for key, value in records["soa_record"].items():
            output.append(f"  {key}: {value}")
    
    return "\n".join(output)

def format_full_output(results: dict, text_format: bool = True) -> str:
    """Format complete analysis results."""
    if not text_format:
        return json.dumps(results, indent=2)
    
    output = []
    
    # Basic info
    output.append("\nBasic Information:")
    output.append("-" * 50)
    for key, value in results["info"].items():
        output.append(f"{key.replace('_', ' ').title()}: {value}")
    
    # URL analysis
    output.append(format_url_output(results["url_analysis"], True))
    
    # DNS analysis
    output.append(format_dns_output(results["dns_analysis"], True))
    
    return "\n".join(output)

def main():
    parser = argparse.ArgumentParser(
        description='Analyze URLs - Get URL components and DNS information'
    )
    parser.add_argument('url', help='URL to analyze')
    parser.add_argument(
        '--mode',
        choices=['url', 'dns', 'full'],
        default='url',
        help='Analysis mode (default: url)'
    )
    parser.add_argument(
        '--format',
        choices=['json', 'text'],
        default='text',
        help='Output format (default: text)'
    )

    args = parser.parse_args()

    try:
        if args.mode == 'url':
            analyzer = URLAnalyzer(args.url)
            results = analyzer.analyze()
            print(format_url_output(results, args.format == 'text'))
            
        elif args.mode == 'dns':
            domain = urlparse(args.url).netloc
            analyzer = DNSAnalyzer(domain)
            results = analyzer.analyze()
            print(format_dns_output(results, args.format == 'text'))
            
        else:  # full analysis
            analyzer = MainAnalyzer(args.url)
            results = analyzer.analyze()
            print(format_full_output(results, args.format == 'text'))
            
    except (URLAnalyzerError, DNSAnalyzerError) as e:
        print(f"Error: {str(e)}")
        exit(1)

if __name__ == '__main__':
    main()
