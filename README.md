# URL Analyzer

A Python tool for analyzing URLs and DNS records.

## Features

- URL Analysis:
  - URL validation and normalization
  - Component extraction (scheme, domain, path, query parameters)
  - Domain parsing

- DNS Analysis:
  - A records (IPv4)
  - AAAA records (IPv6)
  - CNAME records
  - MX records (mail servers)
  - TXT records
  - NS records (nameservers)
  - SOA records

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/url-analyzer.git
cd url-analyzer

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install package
pip install -e .
```

## Usage

### Basic URL Analysis
```bash
# Analyze URL structure (default mode)
url-analyzer https://example.com

# Get JSON output
url-analyzer https://example.com --format json
```

### DNS Analysis
```bash
# Get DNS records
url-analyzer https://example.com --mode dns

# Get DNS records in JSON format
url-analyzer https://example.com --mode dns --format json
```

### Complete Analysis
```bash
# Get both URL and DNS analysis
url-analyzer https://example.com --mode full
```

### Available Modes
- `url`: Analyze URL structure only (default)
- `dns`: Get DNS records only
- `full`: Complete analysis including both URL and DNS

### Output Formats
- `text`: Human-readable format (default)
- `json`: JSON format for programmatic use

## Development

```bash
# Install development dependencies
pip install -r requirements/dev.txt

# Run tests
pytest

# Run linting
make lint

# Format code
make format
```

## License

MIT License
