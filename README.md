# Badar: Personal AI Assistant for Badar Abbas

A personalized AI assistant for Badar Abbas using Retrieval-Augmented Generation (RAG) technology with FAISS vector store, Gemini LLM API, and LangGraph.

## Features

- **Document Processing**: Load and process various document formats (PDF, TXT, DOCX, HTML)
- **Web Retrieval**: Search the web for information related to queries
- **FAISS Vector Store**: Efficient similarity search for document retrieval
- **Gemini LLM Integration**: High-quality text generation using Google's Gemini API
- **LangGraph Workflow**: Orchestrated RAG pipeline with conditional flows
- **High-Quality Prompt Templates**: Optimized prompts for better results
- **Interactive CLI**: User-friendly command-line interface
- **Voice Capabilities**: Speech-to-text and text-to-speech functionality
- **Web Interface**: User-friendly web interface with voice recording and playback

## Installation

1. Clone the repository
2. Install dependencies:
   ```
   pip install -e .
   ```
3. Create a `.env` file with your Gemini API key:
   ```
   GEMINI_API_KEY=your_gemini_api_key_here
   ```

## Usage

### Initialization

Before using the assistant, you need to initialize it with Badar Abbas's personal information:

```bash
# Initialize the assistant
python -m rag-v.main --init
```

### Command Line Interface

```bash
# Add a document to the vector store
python -m rag-v.main --add-file path/to/document.pdf

# Add all documents from a directory
python -m rag-v.main --add-dir path/to/documents

# Ask a question
python -m rag-v.main --question "Who is Badar Abbas?"

# Ask a question without web search
python -m rag-v.main --question "What are Badar's areas of expertise?" --no-web

# Test the RAG system with predefined questions
python -m rag-v.main --test

# Run in interactive mode
python -m rag-v.main
```

### Interactive Mode

In interactive mode, you can:
- Ask questions
- Add documents to the vector store
- Enable/disable web search
- Exit the application

Commands:
- `add file <file_path>`: Add a document to the vector store
- `add dir <directory_path>`: Add documents from a directory
- `web on`: Enable web search
- `web off`: Disable web search
- `exit`: Exit the application

## API Usage

The assistant can also be accessed via a REST API built with FastAPI.

### Starting the API Server

```bash
# Start the API server
python -m rag-v.run_api
```

The web interface will be available at http://localhost:8000/
The API documentation will be available at http://localhost:8000/docs

### API Endpoints

1. **Ask a Question (Text)**
   ```
   POST /ask
   ```
   Request body:
   ```json
   {
     "question": "Who is Badar Abbas?",
     "web_search": true
   }
   ```
   Response:
   ```json
   {
     "answer": "Badar Abbas is a 17-year-old entrepreneur with expertise in business development, Agentic AI, RAG applications, Voice agent AI-based software development, Web development, and App development. He is currently an intermediate student and also serves as the Co-founder and CTO at Lunar AI Studio, a company that provides Agentic AI and Cyber security solutions for all types of industries."
   }
   ```

   Note: The assistant will automatically initialize if needed when you ask a question.

2. **Ask a Question (Voice)**
   ```
   POST /ask-voice
   ```
   Request body:
   ```json
   {
     "audio_base64": "base64_encoded_audio_data",
     "web_search": true
   }
   ```
   Response:
   ```json
   {
     "answer": "Badar Abbas is a 17-year-old entrepreneur...",
     "audio_base64": "base64_encoded_audio_response"
   }
   ```

3. **Upload Audio File**
   ```
   POST /upload-audio
   ```
   Request: Form data with file upload

   Response:
   ```json
   {
     "text": "Transcribed text from the audio file"
   }
   ```

4. **Text to Speech**
   ```
   POST /text-to-speech
   ```
   Request: Form data with `text` field

   Response: Audio file (MP3)

### Example API Usage with cURL

```bash
# Ask a text question
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "What are Badar Abbas'\''s areas of expertise?", "web_search": true}'

# Convert text to speech
curl -X POST http://localhost:8000/text-to-speech \
  -F "text=Hello, this is a test" \
  --output speech.mp3
```

### Example API Usage with Python

```python
import requests
import base64

# Ask a text question
response = requests.post(
    "http://localhost:8000/ask",
    json={"question": "What are Badar Abbas's areas of expertise?", "web_search": True}
)
print(response.json())

# Ask a voice question (assuming you have audio data)
with open("audio_file.wav", "rb") as audio_file:
    audio_data = audio_file.read()
    audio_base64 = base64.b64encode(audio_data).decode('utf-8')

    response = requests.post(
        "http://localhost:8000/ask-voice",
        json={"audio_base64": audio_base64, "web_search": True}
    )

    # Save the audio response
    audio_response = base64.b64decode(response.json()["audio_base64"])
    with open("response.mp3", "wb") as f:
        f.write(audio_response)
```

## Architecture

The application follows a modular architecture:

1. **Document Loading**: Load and process documents from various sources
2. **Web Retrieval**: Search the web for information
3. **Vector Store**: Store and retrieve document embeddings
4. **LLM Integration**: Generate responses using Gemini API
5. **LangGraph Workflow**: Orchestrate the RAG pipeline
6. **Voice Processing**: Handle speech-to-text and text-to-speech conversion
7. **FastAPI Integration**: Expose the assistant's capabilities via a REST API
8. **Web Interface**: Provide a user-friendly interface with voice capabilities

## License

MIT

## Deployment on Vercel

### Prerequisites
1. A Vercel account
2. Git installed on your local machine
3. Vercel CLI installed (`npm i -g vercel`)

### Environment Variables
Before deploying, make sure to set up the following environment variables in your Vercel project settings:
- `GEMINI_API_KEY`: Your Google Gemini API key
- `DEBUG`: Set to "False" for production
- `ENVIRONMENT`: Set to "production"
- `VOICE_ENABLED`: Set to "True" if you want voice capabilities
- `VOICE_LANGUAGE`: Set to "en-US" or your preferred language
- `WEB_SEARCH_ENABLED`: Set to "True" to enable web search
- `MAX_SEARCH_RESULTS`: Set to "5" or your preferred number

### Deployment Steps

1. Clone the repository:
```bash
git clone <your-repository-url>
cd <repository-name>
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Deploy to Vercel:
```bash
vercel
```

4. Follow the prompts to:
   - Log in to your Vercel account
   - Select your project
   - Configure your project settings
   - Deploy

### Project Structure
```
.
├── api.py              # FastAPI application
├── main.py            # Main application logic
├── config.py          # Configuration settings
├── requirements.txt   # Python dependencies
├── vercel.json        # Vercel configuration
├── static/           # Static files (HTML, CSS, JS)
└── data/             # Data files for the assistant
```

### API Endpoints
- `GET /`: Main interface
- `GET /api`: API information
- `POST /ask`: Ask questions
- `POST /ask-voice`: Ask questions with voice response
- `POST /upload-audio`: Upload audio for transcription
- `POST /text-to-speech`: Convert text to speech

### Local Development
To run the project locally:
```bash
uv run uvicorn api:app --reload
```

### Production Deployment
The project is configured for production deployment on Vercel. The `vercel.json` file includes:
- Python build configuration
- Static file serving
- Route handling
- Environment variable setup

### Troubleshooting
1. If you encounter build errors:
   - Check if all dependencies are listed in `requirements.txt`
   - Verify environment variables are set correctly
   - Check Vercel build logs for specific errors

2. If the API is not responding:
   - Verify the API key is set correctly
   - Check if the service is running
   - Review the application logs

3. If static files are not loading:
   - Verify the static directory is properly configured
   - Check file permissions
   - Ensure correct file paths in HTML

### Support
For any issues or questions, please open an issue in the repository.