import argparse
import json
from url_analyzer.core.base_analyzer import BaseURLAnalyzer
from url_analyzer.utils.exceptions import URLAnalyzerError

def main():
    parser = argparse.ArgumentParser(description='Analyze URLs')
    parser.add_argument('url', help='URL to analyze')
    parser.add_argument('--format', choices=['json', 'text'], default='text',
                      help='Output format (default: text)')
    args = parser.parse_args()

    try:
        analyzer = BaseURLAnalyzer(args.url)
        results = analyzer.get_base_info()
        
        if args.format == 'json':
            print(json.dumps(results, indent=2))
        else:
            print("\nURL Analysis Results:")
            print("-" * 50)
            for key, value in results.items():
                print(f"{key.replace('_', ' ').title()}: {value}")
    
    except URLAnalyzerError as e:
        print(f"Error: {str(e)}")
        exit(1)

if __name__ == '__main__':
    main()
