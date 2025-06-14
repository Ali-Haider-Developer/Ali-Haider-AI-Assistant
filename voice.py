"""
Voice capabilities for the RAG application.
"""
import os
import tempfile
import base64
import speech_recognition as sr
import pyttsx3
from pydub import AudioSegment
import io


class VoiceProcessor:
    """
    Class for handling voice processing (speech-to-text and text-to-speech).
    """
    
    def __init__(self):
        """
        Initialize the voice processor.
        """
        self.recognizer = sr.Recognizer()
        # Adjust for ambient noise level
        self.recognizer.energy_threshold = 300
        # Adjust for faster recognition
        self.recognizer.dynamic_energy_threshold = True
        
        # Initialize the TTS engine
        self.engine = pyttsx3.init()
        
        # Get available voices
        voices = self.engine.getProperty('voices')
        
        # Set a female voice if available, otherwise use the default
        for voice in voices:
            if "female" in voice.name.lower():
                self.engine.setProperty('voice', voice.id)
                break
        
        # Adjust speech rate and volume for more natural sound
        self.engine.setProperty('rate', 150)    # Speed of speech
        self.engine.setProperty('volume', 0.9)  # Volume (0.0 to 1.0)
    
    def speech_to_text(self, audio_data):
        """
        Convert speech to text.
        
        Args:
            audio_data: Audio data in bytes.
            
        Returns:
            The recognized text.
        """
        try:
            # Save the audio data to a temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as temp_audio:
                temp_audio.write(audio_data)
                temp_audio_path = temp_audio.name
            
            # Use the recognizer to convert speech to text
            with sr.AudioFile(temp_audio_path) as source:
                audio = self.recognizer.record(source)
                text = self.recognizer.recognize_google(audio)
            
            # Clean up the temporary file
            os.remove(temp_audio_path)
            
            return text
        except sr.UnknownValueError:
            return "Sorry, I could not understand the audio."
        except sr.RequestError as e:
            return f"Sorry, there was an error with the speech recognition service: {e}"
        except Exception as e:
            return f"Error processing audio: {e}"
    
    def text_to_speech(self, text, lang='en'):
        """
        Convert text to speech using pyttsx3 for more natural sound.
        
        Args:
            text: The text to convert to speech.
            lang: The language of the text (not used with pyttsx3).
            
        Returns:
            The audio data in bytes.
        """
        try:
            # Create a temporary file to store the audio
            with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as temp_file:
                temp_path = temp_file.name
            
            # Save the speech to the temporary file
            self.engine.save_to_file(text, temp_path)
            self.engine.runAndWait()
            
            # Read the audio file
            with open(temp_path, 'rb') as audio_file:
                audio_data = audio_file.read()
            
            # Clean up the temporary file
            os.remove(temp_path)
            
            return audio_data
        except Exception as e:
            print(f"Error converting text to speech: {e}")
            return None
    
    def process_audio_file(self, file_path):
        """
        Process an audio file and convert it to text.
        
        Args:
            file_path: Path to the audio file.
            
        Returns:
            The recognized text.
        """
        try:
            # Use the recognizer to convert speech to text
            with sr.AudioFile(file_path) as source:
                audio = self.recognizer.record(source)
                text = self.recognizer.recognize_google(audio)
            
            return text
        except sr.UnknownValueError:
            return "Sorry, I could not understand the audio."
        except sr.RequestError as e:
            return f"Sorry, there was an error with the speech recognition service: {e}"
        except Exception as e:
            return f"Error processing audio file: {e}"
    
    def process_audio_base64(self, audio_base64):
        """
        Process base64-encoded audio data and convert it to text.
        
        Args:
            audio_base64: Base64-encoded audio data.
            
        Returns:
            The recognized text.
        """
        try:
            # Clean the base64 string
            audio_base64 = audio_base64.strip()
            
            # Remove any data URL prefix if present
            if ',' in audio_base64:
                audio_base64 = audio_base64.split(',')[1]
            
            # Add padding if necessary
            missing_padding = len(audio_base64) % 4
            if missing_padding:
                audio_base64 += '=' * (4 - missing_padding)
            
            # Validate base64 string
            try:
                # Try to decode the base64 string
                audio_data = base64.b64decode(audio_base64, validate=True)
            except Exception as e:
                return f"Error decoding base64 audio: {str(e)}"
            
            if not audio_data:
                return "Error: Empty audio data received"
            
            # Convert to WAV format if needed
            try:
                audio = AudioSegment.from_file(io.BytesIO(audio_data))
                wav_data = io.BytesIO()
                audio.export(wav_data, format="wav")
                wav_data.seek(0)
            except Exception as e:
                return f"Error converting audio format: {str(e)}"
            
            # Process the audio data
            text = self.speech_to_text(wav_data.read())
            
            return text
        except Exception as e:
            print(f"Error processing base64 audio: {e}")
            return f"Error processing audio: {e}"
