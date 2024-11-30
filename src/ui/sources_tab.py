import panel as pn
import param
from pathlib import Path
from libs.rag import RAGService

class SourcesTab(param.Parameterized):
    """Document sources management tab"""
    
    def __init__(self, rag_service: RAGService):
        super().__init__()
        self.rag_service = rag_service
        
        # Input widgets for URL-based sources
        self.url_input = pn.widgets.TextInput(
            placeholder="Enter YouTube URL or webpage URL...",
            visible=True
        )
        
        # File upload for PDFs
        self.file_upload = pn.widgets.FileInput(
            accept='.pdf',
            visible=False
        )
        
        # Source type selector
        self.source_type = pn.widgets.Select(
            options=['pdf', 'youtube', 'web'],
            name='Source Type',
            value='pdf'
        )
        
        self.add_button = pn.widgets.Button(
            name="Add Source",
            button_type="primary"
        )
        self.status = pn.pane.Markdown("")
        
        # Bind events
        self.source_type.param.watch(self._handle_type_change, 'value')
        self.add_button.on_click(self._handle_add)
        
    def create(self) -> pn.Column:
        """Create sources interface"""
        return pn.Column(
            pn.Row(pn.pane.Markdown("## Document Sources")),
            pn.Row(
                self.source_type,
                pn.Column(
                    self.url_input,
                    self.file_upload,
                ),
                self.add_button
            ),
            self.status
        )
        
    def _handle_type_change(self, event):
        """Handle source type change"""
        if event.new == 'pdf':
            self.url_input.visible = False
            self.file_upload.visible = True
            self.url_input.placeholder = "Enter YouTube URL or webpage URL..."
        else:
            self.url_input.visible = True
            self.file_upload.visible = False
            placeholder = "Enter YouTube URL..." if event.new == 'youtube' else "Enter webpage URL..."
            self.url_input.placeholder = placeholder
            
    def _handle_add(self, event):
        """Handle add source button click"""
        source_type = self.source_type.value
        
        try:
            if source_type == 'pdf':
                if not self.file_upload.value:
                    self.status.object = "⚠️ Please select a PDF file"
                    return
                    
                # Save uploaded file
                pdf_path = Path(self.rag_service.source_dir) / self.file_upload.filename
                with open(pdf_path, 'wb') as f:
                    f.write(self.file_upload.value)
                source = str(pdf_path)
                
            else:  # youtube or web
                source = self.url_input.value
                if not source:
                    self.status.object = "⚠️ Please enter a URL"
                    return
                    
                # Basic URL validation
                if not source.startswith(('http://', 'https://')):
                    self.status.object = "⚠️ Please enter a valid URL"
                    return
            
            if self.rag_service.add_document(source, source_type):
                self.status.object = f"✅ Successfully added {source_type} source"
                # Clear inputs
                if source_type == 'pdf':
                    self.file_upload.value = None
                else:
                    self.url_input.value = ""
            else:
                self.status.object = "❌ Failed to add source"
                
        except Exception as e:
            self.status.object = f"❌ Error: {str(e)}" 