# Customer Support Chatbot for E-Commerce

An open-source, GPT-style customer support chatbot for a fictional e-commerce store. This project leverages Retrieval-Augmented Generation (RAG), open-source LLMs, FAISS vector search, and a Streamlit frontend to provide document-based question answering, chat memory, and analytics.

## Features

- **Document-based Q&A (RAG):** Answers customer queries using FAQs and product documentation.
- **Chat Memory:** Maintains context across turns for more natural conversations.
- **Open-Source LLM Integration:** Uses Hugging Face Transformers and SentenceTransformers.
- **Vector Search:** Employs FAISS for fast semantic retrieval.
- **Frontend:** Streamlit web app for easy interaction.
- **Basic Analytics:** Tracks chat volume, response quality, and user feedback.
- **Optional:** Multi-lingual support, auto-tagging, knowledge base editing UI.

## Project Structure
<pre>
```plaintext
customer_support_bot/
├── .env                         # Environment variables
├── data/                        # Static and historical data sources
│   ├── chat_logs.json           # Historical customer chat logs
│   ├── faqs.json                # Frequently asked questions
│   └── product_documentation.md # Product documentation
├── main.py                      # Entry point to run the chatbot
├── requirements.txt             # Required Python packages
├── src/                         # Source code
│   ├── database/
│   │   └── vector_store.py      # Vector database management
│   ├── frontend/
│   │   └── app.py               # User-facing application
│   ├── models/
│   │   └── gemini.py            # Language model integration (e.g., Gemini/LLM)
│   └── utils/
│       ├── analytics.py         # Chat data analytics and metrics
│       └── chatbot.py           # Core chatbot logic
└── venv/                        # Python virtual environment (not versioned)
```
</pre>


```

## Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/
customer_support_bot.git
cd customer_support_bot
```
### 2. Create and Activate a Virtual Environment
```
python3 -m venv venv
source venv/bin/activate
```
### 3. Install Dependencies
```
pip install --upgrade pip
pip install -r requirements.txt
``` Apple Silicon (M1/M2/M3) Users
Install PyTorch with Metal backend:

```
pip install --pre torch torchvision torchaudio 
--extra-index-url https://download.pytorch.org/
whl/nightly/cpu
```
### 4. Add Environment Variables
Create a .env file in the root directory and add your Gemini API key:

```
GEMINI_API_KEY=your_gemini_api_key_here
```
### 5. Prepare Data
- Place your FAQs in data/faqs.json (list of Q&A pairs).
- Place product documentation in data/product_documentation.md .
### 6. Run the Application
```
streamlit run src/frontend/app.py
```
## Usage
- Access the chatbot at http://localhost:8501 .
- Ask questions about products, orders, or policies.
- View analytics and chat history.
## Customization
- Knowledge Base: Edit faqs.json and product_documentation.md to update the knowledge base.
- Model: Change the model in vector_store.py or gemini.py for different LLMs.
- Frontend: Modify src/frontend/app.py for UI changes.
## Troubleshooting
- PyTorch Errors on Mac: Ensure you use the correct install command for Apple Silicon.
- Segmentation Faults: Avoid loading models at the top level; use lazy loading and Streamlit caching.
- Streamlit Multiprocessing: Set STREAMLIT_SERVER_NUM_WORKERS=1 if you encounter crashes.
## Contributing
Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

## License
MIT

## Acknowledgments
- Hugging Face Transformers
- SentenceTransformers
- FAISS
- Streamlit
- Google Gemini API
