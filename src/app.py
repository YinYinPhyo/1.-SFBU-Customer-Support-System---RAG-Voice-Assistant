import panel as pn
import param
from typing import Optional
from queue import Queue
import threading

from libs.rag import RAGService
from libs.voice import VoiceService
from src.config import Settings
from src.ui import ChatTab, VoiceTab, SourcesTab

class MultiModalChatApp(param.Parameterized):
    """Combined RAG and Voice Chat Application"""
    
    def __init__(self, settings: Settings):
        super().__init__()
        
        # Initialize services
        self.settings = settings
        self.rag_service = RAGService(
            source_dir=settings.source_dir,
            temp_dir=settings.temp_dir,
            chroma_dir=settings.chroma_dir
        )
        
        self.voice_service = VoiceService(
            api_key=settings.api_key,
            model=settings.whisper_model,
            wake_word=settings.wake_word,
            english=settings.english_only,
            energy=settings.mic_energy,
            pause=settings.mic_pause,
            dynamic_energy=settings.dynamic_energy,
            tts_voice=settings.tts_voice,
            tts_model=settings.tts_model,
            verbose=settings.verbose,
            rag_service=self.rag_service
        )
        
        # Initialize UI components
        self.chat_tab = ChatTab(self.rag_service)
        self.voice_tab = VoiceTab(self.voice_service)
        self.sources_tab = SourcesTab(self.rag_service)
        
        # Create queues for voice processing
        self.audio_queue = Queue()
        self.result_queue = Queue()
        
    def initialize(self) -> bool:
        """Initialize all services"""
        try:
            # Initialize RAG
            if not self.rag_service.initialize():
                raise RuntimeError("Failed to initialize RAG service")
                
            # Initialize voice processing threads
            self._start_voice_threads()
            
            return True
        except Exception as e:
            print(f"Initialization error: {e}")
            return False
            
    def _start_voice_threads(self):
        """Start voice processing threads"""
        threads = [
            (self.voice_service.recorder.record, (self.audio_queue,)),
            (self.voice_service.transcriber.transcribe, (self.audio_queue, self.result_queue)),
            (self.voice_service.responder.process_responses, (self.result_queue,))
        ]
        
        for target, args in threads:
            threading.Thread(target=target, args=args, daemon=True).start()
            
    def create_dashboard(self) -> pn.Column:
        """Create the main dashboard"""
        return pn.Column(
            pn.Row(pn.pane.Markdown('# AI Assistant')),
            pn.Tabs(
                ('Chat', self.chat_tab.create()),
                ('Voice', self.voice_tab.create()),
                ('Sources', self.sources_tab.create())
            )
        ) 