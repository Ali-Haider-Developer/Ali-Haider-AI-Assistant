"""
Document loading and processing functionality.
"""
from typing import List, Optional
import os

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import (
    PyPDFLoader,
    TextLoader,
    Docx2txtLoader,
    UnstructuredHTMLLoader,
    UnstructuredMarkdownLoader,
)

from config import CHUNK_SIZE, CHUNK_OVERLAP


def load_document(file_path: str) -> List:
    """
    Load a document from a file path.

    Args:
        file_path: Path to the document file.

    Returns:
        List of document chunks.
    """
    # Determine file type and use appropriate loader
    _, file_extension = os.path.splitext(file_path)

    if file_extension.lower() == '.pdf':
        loader = PyPDFLoader(file_path)
    elif file_extension.lower() == '.txt':
        loader = TextLoader(file_path, encoding='utf-8')
    elif file_extension.lower() in ['.docx', '.doc']:
        loader = Docx2txtLoader(file_path)
    elif file_extension.lower() in ['.html', '.htm']:
        loader = UnstructuredHTMLLoader(file_path)
    elif file_extension.lower() in ['.md', '.markdown']:
        loader = UnstructuredMarkdownLoader(file_path)
    else:
        # Default to text loader for unknown file types
        print(f"Warning: Unknown file type '{file_extension}' for {file_path}. Using TextLoader as fallback.")
        loader = TextLoader(file_path, encoding='utf-8')

    # Load the document
    documents = loader.load()

    # Split the document into chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
    )

    return text_splitter.split_documents(documents)


def load_documents_from_directory(directory_path: str, file_extensions: Optional[List[str]] = None) -> List:
    """
    Load all documents from a directory.

    Args:
        directory_path: Path to the directory containing documents.
        file_extensions: List of file extensions to include. If None, all supported extensions are included.

    Returns:
        List of document chunks.
    """
    if file_extensions is None:
        file_extensions = ['.pdf', '.txt', '.docx', '.doc', '.html', '.htm', '.md', '.markdown']

    all_documents = []

    for root, _, files in os.walk(directory_path):
        for file in files:
            _, ext = os.path.splitext(file)
            if ext.lower() in file_extensions:
                file_path = os.path.join(root, file)
                try:
                    documents = load_document(file_path)
                    all_documents.extend(documents)
                    print(f"Loaded {file_path}")
                except Exception as e:
                    print(f"Error loading {file_path}: {e}")

    return all_documents
