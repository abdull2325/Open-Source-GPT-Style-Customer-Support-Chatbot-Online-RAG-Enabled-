import json
import os
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
import pickle

class VectorStore:
    def __init__(self, model_name='all-MiniLM-L6-v2'):
        self.model_name = model_name
        self.model = None  # Don't initialize immediately
        self.faiss_index = None
        self.documents = []
        self.index_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data', 'faiss_index')
        self.docs_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data', 'documents.pkl')
    
    def _ensure_model(self):
        """Lazy-load the model only when needed"""
        if self.model is None:
            self.model = SentenceTransformer(self.model_name)
        return self.model

    def load_faqs(self, faq_path):
        with open(faq_path, 'r') as f:
            data = json.load(f)
        
        for faq in data['faqs']:
            self.documents.append({
                'content': f"Question: {faq['question']}\nAnswer: {faq['answer']}",
                'source': 'FAQ',
                'type': 'faq'
            })
    
    def build_index(self):
        if not self.documents:
            raise ValueError("No documents loaded. Please load documents first.")
        
        # Create embeddings for all documents
        texts = [doc['content'] for doc in self.documents]
        embeddings = self._ensure_model().encode(texts)  # Use lazy loading
        
        # Normalize embeddings
        faiss.normalize_L2(embeddings)
        
        # Create FAISS index
        dimension = embeddings.shape[1]
        self.faiss_index = faiss.IndexFlatIP(dimension)
        self.faiss_index.add(embeddings)
        
        # Save index and documents
        self.save_index()
    
    def save_index(self):
        if self.faiss_index is None:
            raise ValueError("No index to save. Please build the index first.")
        
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(self.index_path), exist_ok=True)
        
        # Save FAISS index
        faiss.write_index(self.faiss_index, self.index_path)
        
        # Save documents
        with open(self.docs_path, 'wb') as f:
            pickle.dump(self.documents, f)
    
    def load_index(self):
        if not os.path.exists(self.index_path) or not os.path.exists(self.docs_path):
            raise FileNotFoundError("Index files not found. Please build the index first.")
        
        # Load FAISS index
        self.faiss_index = faiss.read_index(self.index_path)
        
        # Load documents
        with open(self.docs_path, 'rb') as f:
            self.documents = pickle.load(f)
    
    def search(self, query, k=3):
        # Use lazy loading here too
        query_embedding = self._ensure_model().encode([query])
        
        # Normalize query embedding
        faiss.normalize_L2(query_embedding)
        
        # Search index
        scores, indices = self.faiss_index.search(query_embedding, k)
        
        # Get results
        results = []
        for i, idx in enumerate(indices[0]):
            if idx != -1 and scores[0][i] > 0.5:  # Only include relevant results
                results.append({
                    'document': self.documents[idx],
                    'score': float(scores[0][i])
                })
        
        return results