"""
Initialize Badar Abbas's personal assistant.
"""
import os
import sys
import glob

from document_loader import load_document, load_documents_from_directory
from vector_store import VectorStore
from config import GEMINI_API_KEY


def initialize_assistant():
    """
    Initialize the assistant by loading personal information into the vector store.
    """
    # Check if API key is set
    if not GEMINI_API_KEY:
        print("Error: GEMINI_API_KEY environment variable is not set.")
        print("Please set it in a .env file or as an environment variable.")
        return False

    # Create data directory if it doesn't exist
    data_dir = os.path.join(os.path.dirname(__file__), "data")
    os.makedirs(data_dir, exist_ok=True)

    try:
        # Initialize the vector store
        vector_store = VectorStore()

        # Clear existing vector store to ensure fresh data
        print("Clearing existing vector store...")
        vector_store.clear_vector_store()

        # Load all documents from the data directory
        print("Loading documents from data directory...")
        documents = load_documents_from_directory(data_dir)

        if not documents:
            print("No documents found in the data directory.")
            return False

        # Add the documents to the vector store
        print(f"Adding {len(documents)} document chunks to the vector store...")
        vector_store.add_documents(documents)

        print(f"Successfully loaded {len(documents)} document chunks into the vector store.")

        # List the files that were loaded
        print("Loaded files:")
        for file_path in glob.glob(os.path.join(data_dir, "*.*")):
            print(f"  - {os.path.basename(file_path)}")

        # Verify that the vector store was created successfully
        new_vector_store = VectorStore()
        if new_vector_store.vector_store is None:
            print("Error: Vector store was not created successfully.")
            return False

        print("Badar Abbas's personal assistant has been initialized.")
        return True

    except Exception as e:
        import traceback
        print(f"Error initializing assistant: {e}")
        print(traceback.format_exc())
        return False


if __name__ == "__main__":
    success = initialize_assistant()
    sys.exit(0 if success else 1)
