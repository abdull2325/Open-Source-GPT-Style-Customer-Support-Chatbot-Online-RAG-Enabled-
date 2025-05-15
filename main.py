import streamlit as st
import sys
import os

# Add parent directory to path to import modules
sys.path.append(os.path.dirname(__file__))

from src.utils.chatbot import Chatbot
from src.utils.analytics import ChatAnalytics

# Initialize chatbot and analytics
@st.cache_resource
def get_chatbot():
    return Chatbot()

@st.cache_resource
def get_analytics():
    return ChatAnalytics()

chatbot = get_chatbot()
analytics = get_analytics()

# Set up the Streamlit page
st.set_page_config(page_title="E-Commerce Customer Support", page_icon="🛒")

# Your Streamlit app code here
st.title("E-Commerce Customer Support")

# Add your chat interface and other components here

def main():
    # Set the path to the Streamlit app
    app_path = os.path.join(os.path.dirname(__file__), "src", "frontend", "app.py")
    
    # Run the Streamlit app
    sys.argv = ["streamlit", "run", app_path, "--server.port=8501", "--server.address=0.0.0.0"]
    sys.exit(stcli.main())

import os
import sys

# Add the project root to the Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.append(project_root)

# Print instructions for running the app
if __name__ == "__main__":
    print("Please run the app using:")
    print("streamlit run src/frontend/app.py")
    main()