from dataclasses import dataclass
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv
import os

@dataclass
class Settings:
    """Combined application settings"""
    
    # OpenAI Settings
    api_key: str
    
    # RAG Settings
    source_dir: Path = Path("data/sources")
    temp_dir: Path = Path("data/temp")
    chroma_dir: Path = Path("data/chroma")
    
    # Voice Settings
    wake_word: str = "hey abc"
    whisper_model: str = "base"
    english_only: bool = True
    mic_energy: int = 300
    mic_pause: float = 0.8
    dynamic_energy: bool = False
    tts_voice: str = "alloy"
    tts_model: str = "tts-1"
    verbose: bool = True
    
    @classmethod
    def load_from_env(cls) -> 'Settings':
        """Load settings from environment"""
        load_dotenv()
        
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY not found in environment")
            
        return cls(api_key=api_key) 