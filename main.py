"""
Ali Haider's personal AI assistant using RAG technology.
"""
import os
import argparse
from typing import List, Optional

from document_loader import load_document, load_documents_from_directory
from vector_store import VectorStore
from rag_graph import run_rag_graph
from config import GEMINI_API_KEY
from initialize_assistant import initialize_assistant


def add_documents(file_paths: List[str] = None, directory_path: Optional[str] = None) -> None:
    """
    Add documents to the vector store.

    Args:
        file_paths: List of file paths to add.
        directory_path: Directory path to add documents from.
    """
    vector_store = VectorStore()

    if file_paths:
        for file_path in file_paths:
            print(f"Loading {file_path}...")
            documents = load_document(file_path)
            vector_store.add_documents(documents)
            print(f"Added {len(documents)} document chunks from {file_path}")

    if directory_path:
        print(f"Loading documents from {directory_path}...")
        documents = load_documents_from_directory(directory_path)
        vector_store.add_documents(documents)
        print(f"Added {len(documents)} document chunks from {directory_path}")


def ask_question(question: str, web_search: bool = True) -> str:
    """
    Ask a question and get an answer.

    Args:
        question: The question to ask.
        web_search: Whether to enable web search.

    Returns:
        The answer.
    """
    return run_rag_graph(question, web_search_enabled=web_search)


def interactive_mode() -> None:
    """
    Run the application in interactive mode.
    """
    print("=" * 50)
    print("Welcome to Ali Haider's Personal AI Assistant")
    print("=" * 50)
    print("I'm Ali, the AI assistant for Ali Haider.")
    print("I can answer questions about Ali Haider, his work, and expertise.")
    print("I can also help with general questions using my RAG capabilities.")
    print("\nCommands:")
    print("  'exit' - Quit the application")
    print("  'add file <file_path>' - Add a document to my knowledge base")
    print("  'add dir <directory_path>' - Add documents from a directory")
    print("  'web on/off' - Enable/disable web search")
    print("=" * 50)

    web_search = True

    while True:
        user_input = input("\nHow can I assist you today? ")

        if user_input.lower() == 'exit':
            break

        if user_input.lower().startswith('add file '):
            file_path = user_input[9:].strip()
            add_documents(file_paths=[file_path])
            continue

        if user_input.lower().startswith('add dir '):
            directory_path = user_input[8:].strip()
            add_documents(directory_path=directory_path)
            continue

        if user_input.lower() == 'web on':
            web_search = True
            print("Web search enabled")
            continue

        if user_input.lower() == 'web off':
            web_search = False
            print("Web search disabled")
            continue

        # Process the question
        print("\nProcessing your question...")
        answer = ask_question(user_input, web_search=web_search)
        print("\nAnswer:")
        print(answer)


def test_rag_system():
    """
    Test the RAG system with predefined questions.
    """
    print("=" * 70)
    print("Testing Ali Haider's Personal AI Assistant")
    print("=" * 70)

    # Initialize the assistant
    print("Initializing the assistant...")
    success = initialize_assistant()
    if not success:
        print("Failed to initialize the assistant.")
        return

    # Test questions
    test_questions = [
        "Who is Ali Haider?",
        "What is Frellectra AI?",
        "What are Ali's areas of expertise?",
        "What projects has Ali worked on?",
        "What is Ali's role at Frellectra AI?",
        "What technologies does Ali work with?",
    ]

    for i, question in enumerate(test_questions, 1):
        print(f"\nTest Question {i}: {question}")
        print("-" * 70)

        # Ask the question
        answer = ask_question(question, web_search=True)

        print("Answer:")
        print(answer)
        print("=" * 70)


def main():
    """
    Main function.
    """
    # Check if API key is set
    if not GEMINI_API_KEY:
        print("Error: GEMINI_API_KEY environment variable is not set.")
        print("Please set it in a .env file or as an environment variable.")
        return

    parser = argparse.ArgumentParser(description="Ali Haider's Personal AI Assistant")

    # Add arguments
    parser.add_argument("--add-file", dest="add_files", action="append", help="Add a document to the vector store")
    parser.add_argument("--add-dir", dest="add_dir", help="Add documents from a directory to the vector store")
    parser.add_argument("--question", "-q", help="Question to ask")
    parser.add_argument("--no-web", dest="no_web", action="store_true", help="Disable web search")
    parser.add_argument("--init", dest="initialize", action="store_true", help="Initialize Ali Haider's personal assistant")
    parser.add_argument("--test", dest="test", action="store_true", help="Test the RAG system with predefined questions")

    args = parser.parse_args()

    # Process arguments
    if args.test:
        test_rag_system()
        return

    if args.initialize:
        success = initialize_assistant()
        if not success:
            return

    if args.add_files or args.add_dir:
        add_documents(file_paths=args.add_files, directory_path=args.add_dir)

    if args.question:
        answer = ask_question(args.question, web_search=not args.no_web)
        print("\nAnswer:")
        print(answer)
    elif not args.initialize and not args.add_files and not args.add_dir and not args.test:
        # If no specific action is requested, run in interactive mode
        interactive_mode()


if __name__ == "__main__":
    main()
