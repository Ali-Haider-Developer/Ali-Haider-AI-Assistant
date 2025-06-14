#!/bin/bash

# Clean up any existing build artifacts
rm -rf __pycache__
rm -rf .pytest_cache
rm -rf .coverage
rm -rf htmlcov
rm -rf dist
rm -rf build
rm -rf *.egg-info

# Install dependencies with optimizations
pip install --no-cache-dir --no-deps -r requirements.txt

# Create necessary directories
mkdir -p static
mkdir -p vector_store

# Set permissions
chmod -R 755 static
chmod -R 755 vector_store

echo "Build completed successfully!" 