from typing import Dict, Any
from langchain_openai import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate

class RAGChain:
    """Manages the RAG chain for question answering"""
    
    def __init__(self, model_name: str = "gpt-3.5-turbo"):
        self.llm = ChatOpenAI(model=model_name)
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )
        self.chain = None
        
    def create_conversational_chain(self, retriever) -> ConversationalRetrievalChain:
        """Create a conversational chain with the given retriever"""
        template = """
        Answer the question based on the following context:
        {context}
        
        Question: {question}
        """
        
        qa_prompt = PromptTemplate(
            template=template,
            input_variables=["context", "question"]
        )
        
        self.chain = ConversationalRetrievalChain.from_llm(
            llm=self.llm,
            retriever=retriever,
            memory=self.memory,
            combine_docs_chain_kwargs={"prompt": qa_prompt}
        )
        
        return self.chain 