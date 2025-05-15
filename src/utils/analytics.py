import json
import os
from datetime import datetime
import pandas as pd

class ChatAnalytics:
    def __init__(self):
        self.log_file = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data', 'chat_logs.json')
        self.ensure_log_file()
    
    def ensure_log_file(self):
        if not os.path.exists(self.log_file):
            os.makedirs(os.path.dirname(self.log_file), exist_ok=True)
            with open(self.log_file, 'w') as f:
                json.dump([], f)
    
    def log_interaction(self, query, response, context_docs=None, category=None):
        # Auto-categorize if not provided
        if not category:
            category = self.categorize_query(query)
        
        # Create log entry
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'query': query,
            'response': response,
            'category': category,
            'context_used': bool(context_docs and len(context_docs) > 0),
            'context_sources': [doc['document']['source'] for doc in context_docs] if context_docs else []
        }
        
        # Append to log file
        try:
            with open(self.log_file, 'r') as f:
                logs = json.load(f)
            
            logs.append(log_entry)
            
            with open(self.log_file, 'w') as f:
                json.dump(logs, f, indent=2)
        except Exception as e:
            print(f"Error logging interaction: {e}")
    
    def categorize_query(self, query):
        # Simple keyword-based categorization
        query = query.lower()
        
        categories = {
            'shipping': ['shipping', 'delivery', 'track', 'package', 'arrive'],
            'returns': ['return', 'refund', 'money back', 'exchange'],
            'product': ['product', 'item', 'quality', 'broken', 'damaged', 'specs', 'details'],
            'account': ['account', 'login', 'password', 'sign in', 'register', 'profile'],
            'payment': ['payment', 'credit card', 'paypal', 'charge', 'billing', 'invoice'],
            'general': ['help', 'support', 'contact', 'speak', 'human', 'agent']
        }
        
        for category, keywords in categories.items():
            if any(keyword in query for keyword in keywords):
                return category
        
        return 'other'
    
    def get_analytics(self):
        try:
            with open(self.log_file, 'r') as f:
                logs = json.load(f)
            
            if not logs:
                return {
                    'total_interactions': 0,
                    'category_distribution': {},
                    'context_usage': {'with_context': 0, 'without_context': 0}
                }
            
            # Convert to DataFrame for easier analysis
            df = pd.DataFrame(logs)
            
            # Basic analytics
            total = len(df)
            categories = df['category'].value_counts().to_dict()
            context_usage = df['context_used'].value_counts().to_dict()
            
            # Format context usage
            with_context = context_usage.get(True, 0)
            without_context = context_usage.get(False, 0)
            
            return {
                'total_interactions': total,
                'category_distribution': categories,
                'context_usage': {'with_context': with_context, 'without_context': without_context}
            }
        except Exception as e:
            print(f"Error getting analytics: {e}")
            return {
                'total_interactions': 0,
                'category_distribution': {},
                'context_usage': {'with_context': 0, 'without_context': 0},
                'error': str(e)
            }