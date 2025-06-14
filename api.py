"""
FastAPI application for Ali Haider's personal assistant.
"""
from typing import Optional, Dict, Any
from fastapi import FastAPI, HTTPException, Depends, Request, File, UploadFile, Form
from fastapi.responses import HTMLResponse, StreamingResponse, Response
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
import os
import pathlib
import base64
import io

from config import GEMINI_API_KEY
from rag_graph import run_rag_graph
from initialize_assistant import initialize_assistant
from vector_store import VectorStore
from voice import VoiceProcessor


# Check if the API key is set
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY environment variable is not set. Please set it in a .env file.")

# Initialize the FastAPI app
app = FastAPI(
    title="Ali Haider's Personal Assistant API",
    description="API for interacting with Ali Haider's personal AI assistant",
    version="1.0.0",
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

# Get the directory of the current file
current_dir = pathlib.Path(__file__).parent.absolute()

# Create static directory if it doesn't exist
static_dir = os.path.join(current_dir, "static")
os.makedirs(static_dir, exist_ok=True)

# Mount the static files directory
app.mount("/static", StaticFiles(directory=static_dir), name="static")


# Define request and response models
class QuestionRequest(BaseModel):
    """
    Request model for asking a question.
    """
    question: str
    web_search: bool = True


class VoiceQuestionRequest(BaseModel):
    """
    Request model for asking a question via voice.
    """
    question: str
    web_search: bool = True


class AnswerResponse(BaseModel):
    """
    Response model for an answer.
    """
    answer: str


class VoiceAnswerResponse(BaseModel):
    """
    Response model for a voice answer.
    """
    answer: str
    audio_base64: str


class StatusResponse(BaseModel):
    """
    Response model for status messages.
    """
    status: str
    message: str


class TranscriptionResponse(BaseModel):
    """
    Response model for speech-to-text transcription.
    """
    text: str


# Dependency to get or initialize the vector store
def get_vector_store():
    """
    Get the vector store, initializing it if necessary.
    """
    try:
        vector_store = VectorStore()

        # If vector store is not initialized, initialize it automatically
        if vector_store.vector_store is None:
            print("Vector store not initialized. Initializing automatically...")
            success = initialize_assistant()
            if not success:
                raise HTTPException(
                    status_code=500,
                    detail="Failed to initialize the assistant automatically."
                )

            # Refresh the vector store instance after initialization
            vector_store = VectorStore()

            if vector_store.vector_store is None:
                raise HTTPException(
                    status_code=500,
                    detail="Vector store initialization failed."
                )

        return vector_store
    except Exception as e:
        print(f"Error in get_vector_store: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error accessing vector store: {str(e)}"
        )


@app.get("/", response_class=HTMLResponse)
async def root():
    """
    Root endpoint that serves the HTML interface.
    """
    html_file = os.path.join(static_dir, "index.html")
    with open(html_file, "r", encoding="utf-8") as f:
        html_content = f.read()
    return HTMLResponse(content=html_content)


@app.get("/api", response_model=StatusResponse)
async def api_root():
    """
    API root endpoint that returns a welcome message.
    """
    return StatusResponse(
        status="success",
        message="Welcome to Ali Haider's Personal Assistant API. Use /ask to ask questions. The assistant will initialize automatically when needed."
    )


@app.post("/ask", response_model=AnswerResponse)
async def ask_question(request: QuestionRequest, vector_store: VectorStore = Depends(get_vector_store)):
    """
    Endpoint for asking a question to the assistant.
    The vector store will be automatically initialized if needed.
    """
    try:
        # Log the question for debugging
        print(f"Processing question: {request.question}")
        print(f"Web search enabled: {request.web_search}")

        # Import here to ensure we're using the latest configuration
        from llm import get_llm

        # Log the model being used
        llm = get_llm()
        print(f"Using LLM model: {llm.model}")

        # Run the RAG graph to get the answer
        answer = run_rag_graph(request.question, web_search_enabled=request.web_search)

        # Log success
        print(f"Successfully generated answer for question: {request.question}")

        return AnswerResponse(answer=answer)
    except Exception as e:
        # Log the error
        import traceback
        print(f"Error processing question: {request.question}")
        print(f"Error details: {str(e)}")
        print(traceback.format_exc())

        # Return a more user-friendly error message
        error_message = str(e)
        if "Invalid argument provided to Gemini" in error_message:
            error_message = "There was an issue with the Gemini API. Please check your API key and model configuration."

        raise HTTPException(
            status_code=500,
            detail=f"Error processing your question: {error_message}"
        )


@app.post("/ask-voice", response_class=StreamingResponse)
async def ask_question_voice(request: VoiceQuestionRequest, vector_store: VectorStore = Depends(get_vector_store)):
    """
    Endpoint for asking a question and getting the answer as audio.
    Takes text input and returns audio output.
    """
    try:
        # Validate input
        if not request.question:
            raise HTTPException(
                status_code=400,
                detail="No question provided"
            )

        # Log the question
        print(f"Processing question: {request.question}")
        print(f"Web search enabled: {request.web_search}")

        # Run the RAG graph to get the answer
        answer = run_rag_graph(request.question, web_search_enabled=request.web_search)

        # Initialize the voice processor
        voice_processor = VoiceProcessor()

        # Convert the answer to speech
        audio_data = voice_processor.text_to_speech(answer)
        if audio_data is None:
            raise HTTPException(
                status_code=500,
                detail="Failed to convert answer to speech"
            )

        # Return the audio as a streaming response
        return StreamingResponse(
            io.BytesIO(audio_data),
            media_type="audio/mpeg",
            headers={
                "Content-Disposition": "attachment; filename=answer.mp3",
                "X-Answer-Text": answer  # Include the text answer in headers for reference
            }
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        # Log the error
        import traceback
        print(f"Error processing question")
        print(f"Error details: {str(e)}")
        print(traceback.format_exc())

        raise HTTPException(
            status_code=500,
            detail=f"Error processing your question: {str(e)}"
        )


@app.post("/upload-audio", response_model=TranscriptionResponse)
async def upload_audio(file: UploadFile = File(...)):
    """
    Endpoint for uploading an audio file and converting it to text.
    """
    try:
        # Read the audio file
        audio_data = await file.read()

        # Initialize the voice processor
        voice_processor = VoiceProcessor()

        # Convert speech to text
        text = voice_processor.speech_to_text(audio_data)

        return TranscriptionResponse(text=text)
    except Exception as e:
        # Log the error
        import traceback
        print(f"Error processing audio file: {file.filename}")
        print(f"Error details: {str(e)}")
        print(traceback.format_exc())

        raise HTTPException(
            status_code=500,
            detail=f"Error processing audio file: {str(e)}"
        )


@app.post("/text-to-speech", response_class=StreamingResponse)
async def text_to_speech(text: str = Form(...)):
    """
    Endpoint for converting text to speech.
    """
    try:
        # Initialize the voice processor
        voice_processor = VoiceProcessor()

        # Convert text to speech
        audio_data = voice_processor.text_to_speech(text)
        if audio_data is None:
            raise HTTPException(
                status_code=500,
                detail="Failed to convert text to speech"
            )

        # Return the audio as a streaming response
        return StreamingResponse(
            io.BytesIO(audio_data),
            media_type="audio/mpeg",
            headers={"Content-Disposition": "attachment; filename=speech.mp3"}
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        # Log the error
        import traceback
        print(f"Error converting text to speech: {text}")
        print(f"Error details: {str(e)}")
        print(traceback.format_exc())

        raise HTTPException(
            status_code=500,
            detail=f"Error converting text to speech: {str(e)}"
        )


def start():
    """
    Start the FastAPI server.
    """
    uvicorn.run("rag-v.api:app", host="0.0.0.0", port=8000, reload=True)


if __name__ == "__main__":
    start()
