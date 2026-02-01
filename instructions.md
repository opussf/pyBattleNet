pip3 install pytest pytest-cov --target=./packages

# Run tests with coverage
pytest --cov=pybattlenet

# With verbose test output
PYTHONPATH=packages python3 -m pytest --cov=pybattlenet -v

# Generate HTML report (recommended - much easier to read!)
pytest --cov=pybattlenet --cov-report=html

# Generate multiple report types
pytest --cov=pybattlenet --cov-report=html --cov-report=term

# Show missing line numbers in terminal
pytest --cov=pybattlenet --cov-report=term-missing

pip3 install -e . --target=./packages

PYTHONPATH=packages python3 -m pytest --cov=pybattlenet --cov-report=xml:cobertura.xml --cov-report=html  --cov-report=term-missing -v
PYTHONPATH=packages:src python3 -m pytest



pip3 install build --target=./packages
PYTHONPATH=packages python3 -m build --sdist --wheel

