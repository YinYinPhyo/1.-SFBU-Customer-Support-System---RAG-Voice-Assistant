import panel as pn
import param
from libs.voice import VoiceService

class VoiceTab(param.Parameterized):
    """Voice interface tab"""
    
    def __init__(self, voice_service: VoiceService):
        super().__init__()
        self.voice_service = voice_service
        self.chat_display = pn.Column()  # Chat-like display for transcripts
        
        # Start transcript update callback
        self._setup_transcript_callback()
        
    def create(self) -> pn.Column:
        """Create voice tab interface"""
        
        # Voice controls and status
        controls = pn.Column(
            pn.Row(
                pn.pane.Markdown(f"### Wake Word: '{self.voice_service.wake_word}'"),
                pn.pane.Markdown("🎤 Listening...")
            ),
            pn.layout.Divider(),
        )
        
        return pn.Column(
            pn.Row(pn.pane.Markdown("## Voice Interface")),
            controls,
            pn.layout.Divider(),
            self.chat_display
        )
        
    def _setup_transcript_callback(self):
        """Setup callbacks for updating transcripts"""
        def update_transcript(text: str, is_user: bool = True):
            """Add new transcript to display"""
            if not text:
                return
                
            # Format message based on speaker
            speaker = "You" if is_user else "Assistant"
            self.chat_display.append(
                pn.Row(pn.pane.Markdown(f"**{speaker}:** {text}"))
            )
            
        # Register callbacks with voice service
        self.voice_service.transcriber.on_transcribe = lambda text: update_transcript(text, True)
        self.voice_service.responder.on_respond = lambda text: update_transcript(text, False)