from dataclasses import dataclass
from pathlib import Path
import whisper
from .recorder import AudioRecorder
from .transcriber import Transcriber
from .responder import Responder
from typing import Optional

@dataclass
class VoiceService:
    """Main service for voice functionality"""
    
    api_key: str
    model: str
    wake_word: str
    english: bool
    energy: int
    pause: float
    dynamic_energy: bool
    tts_voice: str
    tts_model: str
    verbose: bool
    rag_service: Optional['RAGService'] = None
    
    def __post_init__(self):
        # Initialize whisper model
        self.whisper_model = whisper.load_model(self.model)
        
        # Initialize components
        self.recorder = AudioRecorder(
            energy=self.energy,
            pause=self.pause,
            dynamic_energy=self.dynamic_energy
        )
        
        self.transcriber = Transcriber(
            model=self.whisper_model,
            wake_word=self.wake_word,
            english=self.english,
            rag_service=self.rag_service
        )
        
        self.responder = Responder(
            api_key=self.api_key,
            temp_dir=Path("temp"),
            voice=self.tts_voice,
            model=self.tts_model
        ) 