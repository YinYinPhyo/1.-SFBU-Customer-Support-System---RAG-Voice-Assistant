from pathlib import Path
from typing import List, Optional
from langchain.docstore.document import Document
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores.chroma import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter

class RAGVectorStore:
    """Manages the vector store for document embeddings"""
    
    def __init__(self, persist_directory: Path):
        self.persist_directory = persist_directory
        self.embeddings = OpenAIEmbeddings()
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=150
        )
        self.vectorstore = Chroma(
            persist_directory=str(self.persist_directory),
            embedding_function=self.embeddings
        )
        
    def initialize(self) -> bool:
        """Initialize or load the vector store"""
        try:
            if not self.vectorstore:
                self.vectorstore = Chroma(
                    persist_directory=str(self.persist_directory),
                    embedding_function=self.embeddings
                )
            return True
        except Exception as e:
            print(f"Vector store initialization error: {e}")
            return False
            
    def add_documents(self, documents: List[Document]) -> bool:
        """Add documents to the vector store"""
        try:
            splits = self.text_splitter.split_documents(documents)
            self.vectorstore.add_documents(splits)
            return True
        except Exception as e:
            print(f"Error adding documents: {e}")
            return False
            
    def as_retriever(self, **kwargs):
        """Get the retriever interface"""
        return self.vectorstore.as_retriever(**kwargs) 