"""
Gemini LLM API integration.
"""
from langchain_google_genai import ChatGoogleGenerativeAI
import google.generativeai as genai

from config import GEMINI_API_KEY


def initialize_gemini():
    """
    Initialize the Gemini API.
    """
    genai.configure(api_key=GEMINI_API_KEY)


def get_llm(model_name: str = "gemini-1.5-flash", temperature: float = 0.2):
    """
    Get the LLM model.

    Args:
        model_name: Name of the model to use.
        temperature: Temperature for generation.

    Returns:
        The LLM model.
    """
    # Initialize Gemini API
    initialize_gemini()

    # Create LLM
    return ChatGoogleGenerativeAI(
        model=model_name,
        temperature=temperature,
        google_api_key=GEMINI_API_KEY,
        convert_system_message_to_human=True,
    )
