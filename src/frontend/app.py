import streamlit as st
import sys
import os

# Add parent directory to path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from src.utils.chatbot import Chatbot
from src.utils.analytics import ChatAnalytics

# Initialize chatbot and analytics with proper error handling
@st.cache_resource(show_spinner="Loading AI models...")
def get_chatbot():
    try:
        return Chatbot()
    except Exception as e:
        st.error(f"Error initializing chatbot: {str(e)}")
        return None

@st.cache_resource(ttl=3600)  # Cache for 1 hour
def get_analytics():
    try:
        return ChatAnalytics()
    except Exception as e:
        st.error(f"Error initializing analytics: {str(e)}")
        return None

# Initialize components with error handling
try:
    chatbot = get_chatbot()
    analytics = get_analytics()
    if not chatbot or not analytics:
        st.error("Failed to initialize required components")
        st.stop()
except Exception as e:
    st.error(f"Initialization error: {str(e)}")
    st.stop()

# Set up the Streamlit page
st.set_page_config(page_title="E-Commerce Customer Support", page_icon="🛒")

# Sidebar for analytics and options
with st.sidebar:
    st.title("📊 Chat Analytics")
    
    # Get analytics data
    analytics_data = analytics.get_analytics()
    
    st.metric("Total Interactions", analytics_data['total_interactions'])
    
    # Category distribution
    st.subheader("Query Categories")
    for category, count in analytics_data['category_distribution'].items():
        st.text(f"{category.capitalize()}: {count}")
    
    # Context usage
    st.subheader("Knowledge Base Usage")
    st.text(f"Queries using KB: {analytics_data['context_usage']['with_context']}")
    st.text(f"General queries: {analytics_data['context_usage']['without_context']}")
    
    # Reset chat button
    if st.button("Reset Chat"):
        chatbot.reset_chat()
        st.session_state.messages = []
        st.success("Chat history has been reset!")

# Main chat interface
st.title("🛒 E-Commerce Customer Support")
st.caption("Ask questions about products, shipping, returns, and more!")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("How can I help you today?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        
        # Get response from chatbot
        result = chatbot.process_query(prompt)
        response = result['response']
        
        # Display response
        message_placeholder.markdown(response)
    
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})