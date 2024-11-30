from typing import List, Optional
from pathlib import Path
import os
from langchain.docstore.document import Document
from langchain_community.document_loaders import (
    PyPDFLoader,
    YoutubeAudioLoader,
    WebBaseLoader
)
from langchain_community.document_loaders.generic import GenericLoader
from langchain.document_loaders.parsers import OpenAIWhisperParser

class RAGLoader:
    """Handles loading documents from various sources"""
    
    def __init__(self, temp_dir: Path):
        self.temp_dir = temp_dir
        os.makedirs(temp_dir, exist_ok=True)
        
    def load_pdf(self, file_path: str) -> List[Document]:
        """Load PDF document"""
        loader = PyPDFLoader(file_path)
        return loader.load()
        
    def load_youtube(self, url: str) -> List[Document]:
        """Load YouTube content"""
        audio_loader = YoutubeAudioLoader([url], str(self.temp_dir))
        whisper_parser = OpenAIWhisperParser()
        loader = GenericLoader(audio_loader, whisper_parser)
        documents = loader.load()
        
        for doc in documents:
            doc.metadata["source"] = url
            doc.metadata["source_type"] = "YouTube"
            
        return documents
        
    def load_webpage(self, url: str) -> List[Document]:
        """Load webpage content"""
        loader = WebBaseLoader(url)
        documents = loader.load()
        
        for doc in documents:
            doc.metadata["source"] = url
            doc.metadata["source_type"] = "Web"
            
        return documents 