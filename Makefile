.PHONY: clean deps dev-deps test lint format

clean:
		find . -type d -name "pycache" -exec rm -rf {} +
		find . -type f -name ".pyc" -delete
		find . -type f -name ".pyo" -delete
		find . -type f -name ".pyd" -delete
		find . -type f -name ".coverage" -delete
		find . -type d -name ".egg-info" -exec rm -rf {} +
		find . -type d -name "*.egg" -exec rm -rf {} +
		find . -type d -name ".pytest_cache" -exec rm -rf {} +
		find . -type d -name "htmlcov" -exec rm -rf {} +

deps:
		pip install -r requirements/base.txt

dev-deps:
		pip install -r requirements/dev.txt

test:
		pytest

lint:
		flake8 src tests
		black --check src tests
		isort --check-only src tests

format:
		black src tests
		isort src tests
