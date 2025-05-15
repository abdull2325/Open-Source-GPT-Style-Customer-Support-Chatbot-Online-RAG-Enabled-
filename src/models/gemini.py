import os
import google.generativeai as genai
from dotenv import load_dotenv

class GeminiBot:
    def __init__(self):
        load_dotenv()
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-pro')
        self.chat_history = []
    
    def generate_response(self, query, context_docs=None):
        # Prepare prompt with context documents if available
        if context_docs and len(context_docs) > 0:
            context = "\n\n".join([doc['document']['content'] for doc in context_docs])
            system_prompt = f"""You are a helpful customer support assistant for an e-commerce store. 
            Use the following information to answer the user's question. 
            If you don't know the answer based on the provided information, say so politely and offer to connect them with a human agent.
            
            CONTEXT INFORMATION:
            {context}
            
            Answer the user's question based on the above context. Be concise, helpful, and friendly."""
        else:
            system_prompt = """You are a helpful customer support assistant for an e-commerce store. 
            Answer the user's question to the best of your ability. If you don't know the answer, say so politely and offer to connect them with a human agent.
            Be concise, helpful, and friendly."""
        
        # Add chat history for context if available
        chat = self.model.start_chat(history=self.chat_history)
        
        # Generate response
        response = chat.send_message(f"{system_prompt}\n\nUser: {query}")
        
        # Update chat history
        self.chat_history.append({"role": "user", "parts": [query]})
        self.chat_history.append({"role": "model", "parts": [response.text]})
        
        # Limit chat history to last 10 messages to avoid token limits
        if len(self.chat_history) > 10:
            self.chat_history = self.chat_history[-10:]
        
        return response.text
    
    def reset_chat(self):
        self.chat_history = []