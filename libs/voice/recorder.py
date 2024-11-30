from dataclasses import dataclass
import speech_recognition as sr
from queue import Queue
import numpy as np
import io
import wave

@dataclass
class AudioRecorder:
    """Handles audio recording from microphone"""
    
    energy: int
    pause: float
    dynamic_energy: bool
    sample_rate: int = 16000
    
    def __post_init__(self):
        self.recognizer = sr.Recognizer()
        self.recognizer.energy_threshold = self.energy
        self.recognizer.pause_threshold = self.pause
        self.recognizer.dynamic_energy_threshold = self.dynamic_energy
        
    def record(self, audio_queue: Queue) -> None:
        """Record audio and add to queue"""
        with sr.Microphone(sample_rate=self.sample_rate) as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
            
            while True:
                try:
                    audio = self.recognizer.listen(source)
                    if hasattr(audio, 'get_wav_data'):
                        # Convert wav data to numpy array
                        wav_data = io.BytesIO(audio.get_wav_data())
                        with wave.open(wav_data, 'rb') as wav_file:
                            audio_data = np.frombuffer(
                                wav_file.readframes(wav_file.getnframes()), 
                                dtype=np.int16
                            )
                            audio_data = audio_data.astype(np.float32) / 32768.0
                        audio_queue.put_nowait(audio_data)
                    else:
                        print("Warning: Audio data format not supported")
                except Exception as e:
                    print(f"Recording error: {e}")
                    continue 