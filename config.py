"""
Configuration settings for the RAG application.
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Gemini API key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Vector store settings
VECTOR_STORE_PATH = "vector_store"

# Embedding settings
EMBEDDING_MODEL = "models/embedding-001"  # Gemini embedding model

# Document processing settings
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200

# RAG settings
TOP_K_RESULTS = 100  # Number of results to retrieve from vector store

# Web retrieval settings
MAX_SEARCH_RESULTS = 5  # Number of search results to process
