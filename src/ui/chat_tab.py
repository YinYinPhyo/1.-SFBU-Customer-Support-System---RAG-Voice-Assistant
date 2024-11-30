import panel as pn
import param
from libs.rag import RAGService

class ChatTab(param.Parameterized):
    """Chat interface tab"""
    
    def __init__(self, rag_service: RAGService):
        super().__init__()
        self.rag_service = rag_service
        self.chat_history = []
        self.input = pn.widgets.TextInput(placeholder="Type your message...")
        self.send_button = pn.widgets.Button(name="Send", button_type="primary")
        self.chat_display = pn.Column()
        
        self.send_button.on_click(self._handle_send)
        
    def create(self) -> pn.Column:
        """Create chat interface"""
        return pn.Column(
            pn.Row(pn.pane.Markdown("## Chat")),
            self.chat_display,
            pn.Row(
                self.input,
                self.send_button
            )
        )
        
    def _handle_send(self, event):
        """Handle send button click"""
        question = self.input.value
        if not question:
            return
            
        # Add user message to display
        self.chat_display.append(
            pn.Row(pn.pane.Markdown(f"**You:** {question}"))
        )
        
        # Get answer from RAG
        result = self.rag_service.get_answer(question)
        answer = result.get('answer', 'Sorry, I could not generate an answer.')
        
        # Add assistant response to display
        self.chat_display.append(
            pn.Row(pn.pane.Markdown(f"**Assistant:** {answer}"))
        )
        
        # Clear input
        self.input.value = "" 