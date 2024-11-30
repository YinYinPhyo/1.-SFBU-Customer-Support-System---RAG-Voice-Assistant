from dataclasses import dataclass
from pathlib import Path
from queue import Queue
import os
from openai import OpenAI
from pydub import AudioSegment
from pydub.playback import play

@dataclass
class Responder:
    """Handles text-to-speech conversion and playback"""
    
    api_key: str
    temp_dir: Path
    voice: str = "alloy"
    model: str = "tts-1"
    
    def __post_init__(self):
        self.client = OpenAI(api_key=self.api_key)
        self.temp_dir.mkdir(parents=True, exist_ok=True)
        self.on_respond = lambda _: None  # Callback for response updates
        
    def process_responses(self, result_queue: Queue) -> None:
        """Process responses from queue"""
        while True:
            text = result_queue.get()
            try:
                # Notify UI of new response
                self.on_respond(text)
                # Convert to speech and play
                self.speak(text)
            except Exception as e:
                print(f"Response error: {e}")
                continue
                
    def speak(self, text: str) -> None:
        """Convert text to speech and play it"""
        audio_file = self.temp_dir / f"response_{hash(text)}.mp3"
        
        try:
            # Generate speech
            response = self.client.audio.speech.create(
                model=self.model,
                voice=self.voice,
                input=text
            )
            
            # Save and play audio
            response.stream_to_file(str(audio_file))
            audio = AudioSegment.from_mp3(str(audio_file))
            play(audio)
            
        except Exception as e:
            print(f"Speech generation error: {e}")
            raise
        finally:
            audio_file.unlink(missing_ok=True) 