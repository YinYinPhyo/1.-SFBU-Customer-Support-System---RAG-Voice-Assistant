from dataclasses import dataclass
from queue import Queue
import whisper
import re
from typing import Optional

@dataclass
class Transcriber:
    """Handles speech-to-text conversion"""
    
    model: whisper.Whisper
    wake_word: str
    english: bool
    rag_service: Optional['RAGService'] = None
    
    def __post_init__(self):
        self.on_transcribe = lambda _: None  # Callback for transcript updates
    
    def transcribe(self, audio_queue: Queue, result_queue: Queue) -> None:
        """Transcribe audio from queue"""
        while True:
            audio_data = audio_queue.get()
            
            try:
                result = self.model.transcribe(
                    audio_data,
                    language='english' if self.english else None,
                    fp16=False
                )
                
                text = result["text"].strip()
                if self._contains_wake_word(text):
                    question = self._clean_text(text)
                    
                    # Notify UI of new transcript
                    self.on_transcribe(question)
                    
                    # Get answer from RAG if available
                    if self.rag_service:
                        rag_response = self.rag_service.get_answer(question)
                        answer = rag_response.get('answer', 
                            'Sorry, I could not generate an answer.')
                    else:
                        answer = question  # Fallback to echo if no RAG
                        
                    result_queue.put_nowait(answer)
                    
            except Exception as e:
                print(f"Transcription error: {e}")
                continue
                
    def _contains_wake_word(self, text: str) -> bool:
        """Check if text contains wake word"""
        return text.lower().startswith(self.wake_word.lower())
        
    def _clean_text(self, text: str) -> str:
        """Clean transcribed text"""
        # Remove wake word
        pattern = re.compile(re.escape(self.wake_word), re.IGNORECASE)
        text = pattern.sub("", text).strip()
        
        # Remove punctuation
        text = re.sub(r'[^\w\s]', '', text)
        
        return text 