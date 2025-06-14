#!/bin/bash

# Upgrade pip
python -m pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt

# Create necessary directories
mkdir -p static
mkdir -p vector_store

# Set permissions
chmod -R 755 static
chmod -R 755 vector_store

echo "Build completed successfully!" 