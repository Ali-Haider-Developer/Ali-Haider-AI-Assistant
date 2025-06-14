"""
Script to run the FastAPI server for Badar Abbas's personal assistant.
"""
import uvicorn
import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def check_environment():
    """
    Check if the environment is properly set up.
    """
    # Check if the API key is set
    if not os.getenv("GEMINI_API_KEY"):
        print("Error: GEMINI_API_KEY environment variable is not set.")
        print("Please set it in a .env file or as an environment variable.")
        return False

    # Check the LLM configuration
    try:
        from llm import get_llm
        llm = get_llm()
        print(f"Using LLM model: {llm.model}")

        # Verify that we're using Gemini Flash 1.5
        if "flash" not in llm.model:
            print(f"Warning: You are using {llm.model}, but Gemini Flash 1.5 is recommended.")
            print("Updating LLM configuration to use Gemini Flash 1.5...")

            # Update the llm.py file to use Gemini Flash 1.5
            from llm import get_llm
            llm = get_llm(model_name="gemini-1.5-flash")
            print(f"Updated LLM model to: {llm.model}")
    except Exception as e:
        print(f"Warning: Could not check LLM configuration: {e}")

    # Check if the data directory exists
    data_dir = os.path.join(os.path.dirname(__file__), "data")
    if not os.path.exists(data_dir):
        print(f"Warning: Data directory does not exist: {data_dir}")
        print("Creating data directory...")
        os.makedirs(data_dir, exist_ok=True)

    # Check if there are any files in the data directory
    files = [f for f in os.listdir(data_dir) if os.path.isfile(os.path.join(data_dir, f))]
    if not files:
        print(f"Warning: No files found in data directory: {data_dir}")
        print("The assistant may not have any knowledge to work with.")
    else:
        print(f"Found {len(files)} files in data directory.")

    return True

if __name__ == "__main__":
    # Check environment
    if not check_environment():
        sys.exit(1)

    print("=" * 70)
    print("Starting Badar Abbas's Personal Assistant...")
    print("=" * 70)
    print("Web Interface: http://localhost:8000/")
    print("API Documentation: http://localhost:8000/docs")
    print("=" * 70)
    print("Press Ctrl+C to stop the server")

    try:
        uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)
    except Exception as e:
        import traceback
        print(f"Error starting server: {e}")
        print(traceback.format_exc())
        sys.exit(1)
