"""
FAISS vector store functionality.
"""
from typing import List, Optional
import os

from langchain_community.vectorstores import FAISS
from langchain.schema.document import Document

from embeddings import get_embedding_model, get_document_embedding_model
from config import VECTOR_STORE_PATH, TOP_K_RESULTS


class VectorStore:
    """
    Class for managing the FAISS vector store.
    """

    def __init__(self, persist_directory: Optional[str] = None):
        """
        Initialize the vector store.

        Args:
            persist_directory: Directory to persist the vector store. If None, uses the default.
        """
        self.persist_directory = persist_directory or VECTOR_STORE_PATH
        self.embedding_model = get_document_embedding_model()
        self.query_embedding_model = get_embedding_model()

        # Create persist directory if it doesn't exist
        os.makedirs(self.persist_directory, exist_ok=True)

        # Initialize or load the vector store
        if os.path.exists(self.persist_directory) and os.listdir(self.persist_directory):
            try:
                self.vector_store = self.load_vector_store()
                if self.vector_store is None:
                    print(f"Failed to load vector store from {self.persist_directory}. Will create a new one when documents are added.")
            except Exception as e:
                print(f"Error loading vector store: {e}")
                self.vector_store = None
        else:
            self.vector_store = None

    def add_documents(self, documents: List[Document]) -> None:
        """
        Add documents to the vector store.

        Args:
            documents: List of documents to add.
        """
        if not documents:
            print("Warning: No documents provided to add_documents.")
            return

        try:
            if self.vector_store is None:
                # Create a new vector store
                print(f"Creating new vector store with {len(documents)} documents...")
                self.vector_store = FAISS.from_documents(
                    documents=documents,
                    embedding=self.embedding_model,
                )
                print("Vector store created successfully.")
            else:
                # Add to existing vector store
                print(f"Adding {len(documents)} documents to existing vector store...")
                self.vector_store.add_documents(documents)
                print("Documents added successfully.")

            # Persist the vector store
            print("Persisting vector store to disk...")
            self.persist_vector_store()
            print(f"Vector store persisted to {self.persist_directory}")
        except Exception as e:
            import traceback
            print(f"Error adding documents to vector store: {e}")
            print(traceback.format_exc())

    def similarity_search(self, query: str, k: Optional[int] = None) -> List[Document]:
        """
        Perform a similarity search.

        Args:
            query: The query string.
            k: Number of results to return. If None, uses the default.

        Returns:
            List of similar documents.
        """
        if self.vector_store is None:
            return []

        k = k or TOP_K_RESULTS

        # Use the query embedding model for search
        return self.vector_store.similarity_search(
            query=query,
            k=k,
        )

    def persist_vector_store(self) -> None:
        """
        Persist the vector store to disk.
        """
        if self.vector_store is not None:
            try:
                # Create directory if it doesn't exist
                os.makedirs(self.persist_directory, exist_ok=True)

                # Save the vector store
                self.vector_store.save_local(self.persist_directory)
                print(f"Vector store saved to {self.persist_directory}")
            except Exception as e:
                import traceback
                print(f"Error persisting vector store: {e}")
                print(traceback.format_exc())

    def load_vector_store(self) -> FAISS:
        """
        Load the vector store from disk.

        Returns:
            The loaded vector store.
        """
        try:
            return FAISS.load_local(
                folder_path=self.persist_directory,
                embeddings=self.embedding_model
            )
        except Exception as e:
            print(f"Error loading vector store: {e}")
            return None

    def clear_vector_store(self) -> None:
        """
        Clear the vector store.
        """
        try:
            if os.path.exists(self.persist_directory):
                import shutil
                print(f"Removing vector store directory: {self.persist_directory}")
                shutil.rmtree(self.persist_directory)
                print("Vector store directory removed successfully.")
            else:
                print(f"Vector store directory does not exist: {self.persist_directory}")

            self.vector_store = None
        except Exception as e:
            import traceback
            print(f"Error clearing vector store: {e}")
            print(traceback.format_exc())
