from pathlib import Path
from typing import Dict, Any, List, Optional
from langchain.docstore.document import Document
from .loader import RAGLoader
from .vectorstore import RAGVectorStore
from .chain import RAGChain

class RAGService:
    """Main service for RAG functionality"""
    
    def __init__(self, source_dir: Path, temp_dir: Path, chroma_dir: Path):
        self.source_dir = source_dir
        self.temp_dir = temp_dir
        self.chroma_dir = chroma_dir
        
        # Create directories
        for dir_path in [source_dir, temp_dir, chroma_dir]:
            dir_path.mkdir(parents=True, exist_ok=True)
            
        self.loader = RAGLoader(temp_dir)
        self.vectorstore = RAGVectorStore(chroma_dir)
        self.chain = RAGChain()
        
    def initialize(self) -> bool:
        """Initialize the service"""
        try:
            self.vectorstore.initialize()
            return True
        except Exception as e:
            print(f"Initialization error: {e}")
            return False
            
    def add_document(self, source: str, source_type: str) -> bool:
        """Add a document to the system"""
        try:
            if source_type == "pdf":
                docs = self.loader.load_pdf(source)
            elif source_type == "youtube":
                docs = self.loader.load_youtube(source)
            elif source_type == "web":
                docs = self.loader.load_webpage(source)
            else:
                raise ValueError(f"Unsupported source type: {source_type}")
                
            self.vectorstore.add_documents(docs)
            return True
        except Exception as e:
            print(f"Error adding document: {e}")
            return False
            
    def get_answer(self, question: str) -> Dict[str, Any]:
        """Get answer for a question"""
        try:
            chain = self.chain.create_conversational_chain(self.vectorstore.as_retriever())
            return chain({"question": question})
        except Exception as e:
            print(f"Error getting answer: {e}")
            return {
                "answer": "Sorry, I encountered an error processing your question.",
                "source_documents": []
            } 