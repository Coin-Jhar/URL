from url_analyzer.core.base_analyzer import BaseURLAnalyzer

def analyze_url(url):
    """Demonstrate basic URL analysis."""
    # Create analyzer
    analyzer = BaseURLAnalyzer(url)
    
    # Get basic information
    info = analyzer.get_base_info()
    print("\nBasic URL Information:")
    print("-" * 50)
    for key, value in info.items():
        print(f"{key}: {value}")
    
    # Get domain
    print("\nDomain Information:")
    print("-" * 50)
    print(f"Main domain: {analyzer.get_domain()}")
    
    # Get normalized URL
    print("\nURL Normalization:")
    print("-" * 50)
    print(f"Original URL: {url}")
    print(f"Normalized URL: {analyzer.normalized_url}")

if __name__ == "__main__":
    # Example URLs
    urls = [
        "https://example.com/path?param=value",
        "HTTP://ExAmPlE.com/",
        "https://sub.example.co.uk/path?a=1&b=2",
    ]
    
    for url in urls:
        print("\n" + "=" * 60)
        print(f"Analyzing URL: {url}")
        analyze_url(url)
