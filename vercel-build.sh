#!/bin/bash

# Upgrade pip and install build tools
python -m pip install --upgrade pip setuptools wheel

# Install dependencies
python -m pip install fastapi==0.109.2 uvicorn==0.27.1 pydantic==2.6.1 python-multipart==0.0.9 python-dotenv==1.0.1 langchain==0.1.9 langchain-community==0.0.24 langchain-google-genai==0.0.11 langchain-text-splitters==0.0.1 langgraph==0.0.24 google-generativeai>=0.4.1,<0.5.0 beautifulsoup4==4.12.3 requests==2.31.0 unstructured==0.10.30 pypdf==4.0.1 docx2txt==0.8 tiktoken==0.6.0 SpeechRecognition==3.10.1 gTTS==2.5.1 pydub==0.25.1 websockets==12.0 pyttsx3==2.90

# Create necessary directories
mkdir -p static
mkdir -p vector_store

# Set permissions
chmod -R 755 static
chmod -R 755 vector_store

echo "Build completed successfully!" 