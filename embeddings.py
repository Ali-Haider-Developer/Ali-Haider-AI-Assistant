"""
Embedding models for vectorizing text.
"""
from langchain_google_genai import GoogleGenerativeAIEmbeddings

from config import GEMINI_API_KEY, EMBEDDING_MODEL


def get_embedding_model():
    """
    Get the embedding model.
    
    Returns:
        The embedding model.
    """
    return GoogleGenerativeAIEmbeddings(
        model=EMBEDDING_MODEL,
        google_api_key=GEMINI_API_KEY,
        task_type="retrieval_query",  # For query embeddings
    )


def get_document_embedding_model():
    """
    Get the embedding model for documents.
    
    Returns:
        The embedding model for documents.
    """
    return GoogleGenerativeAIEmbeddings(
        model=EMBEDDING_MODEL,
        google_api_key=GEMINI_API_KEY,
        task_type="retrieval_document",  # For document embeddings
    )
