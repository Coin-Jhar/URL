# URL Analyzer

A Python tool for analyzing URLs, extracting components, and validating structure.

## Features

- URL validation and normalization
- Component extraction (scheme, domain, path, query parameters)
- Domain parsing
- Command-line interface

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

### Command Line
```bash
# Basic URL analysis
url-analyzer https://example.com/path?param=value

# JSON output
url-analyzer --format json https://example.com/path?param=value
```

### Python API
```python
from url_analyzer.core.base_analyzer import BaseURLAnalyzer

# Create analyzer
analyzer = BaseURLAnalyzer("https://example.com/path?param=value")

# Get URL info
info = analyzer.get_base_info()

# Get domain
domain = analyzer.get_domain()
```

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
