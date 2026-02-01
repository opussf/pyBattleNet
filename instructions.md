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

pip3 install -e . --target=./packages --upgrade

PYTHONPATH=packages python3 -m pytest --cov=pybattlenet --cov-report=xml:cobertura.xml --cov-report=html  --cov-report=term-missing -v
PYTHONPATH=packages:src python3 -m pytest



pip3 install build --target=./packages
PYTHONPATH=packages python3 -m build --sdist --wheel


pip3 install flake8 --target=./packages
PYTHONPATH=packages python3 -m flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics