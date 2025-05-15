from ..database.vector_store import VectorStore
from ..models.gemini import GeminiBot
from .analytics import ChatAnalytics
import os

class Chatbot:
    def __init__(self):
        self.vector_store = VectorStore()
        self.gemini_bot = GeminiBot()
        self.analytics = ChatAnalytics()
        self.initialize_knowledge_base()
    
    def initialize_knowledge_base(self):
        # Check if index exists, if not build it
        try:
            self.vector_store.load_index()
            print("Knowledge base loaded successfully!")
        except FileNotFoundError:
            print("Building knowledge base...")
            # Load FAQs and documentation
            faq_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data', 'faqs.json')
            doc_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data', 'product_documentation.md')
            
            self.vector_store.load_faqs(faq_path)
            self.vector_store.load_documentation(doc_path)
            self.vector_store.build_index()
            print("Knowledge base built successfully!")
    
    def process_query(self, query):
        # Search for relevant documents
        context_docs = self.vector_store.search(query, k=3)
        
        # Generate response using Gemini
        response = self.gemini_bot.generate_response(query, context_docs)
        
        # Log interaction for analytics
        self.analytics.log_interaction(query, response, context_docs)
        
        return {
            'response': response,
            'context_docs': context_docs
        }
    
    def reset_chat(self):
        self.gemini_bot.reset_chat()
        return {"status": "Chat history reset successfully"}