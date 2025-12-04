import whisper
import os



class WhisperModelSingleton:
    """Singleton pattern for Whisper Model - only laos ovce"""
    _instance = None
    _model = None

    def __new__(cls, model_size='base'):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            print(f"Loading Whisper model '{model_size}'... ")
            cls._model = whisper.load_model(model_size)
            print("Whisper model loaded successfully!")
        return cls._instance

    @property
    def model(self):
        return self._model

class TranscriptionService:
    """Handles audio transcription with Whisper AI"""

    """Initializes the transcription model"""
    def __init__(self, model_size='base'):
        self.model = WhisperModelSingleton(model_size).model

    def transcribe_audio(self, audio_path):
        """Transcript Audio-Data to Text"""
        result = self.model.transcribe(audio_path)
        return result['text']

    def transcribe_and_cleanup(self, audio_path):
        """Transcript and Delete Audio-Data afterwards"""
        try:
            transcript = self.transcribe_audio(audio_path)
            return transcript
        finally:
            if os.path.exists(audio_path):
                os.remove(audio_path)