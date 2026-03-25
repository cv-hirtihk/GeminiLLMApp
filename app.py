from dotenv import load_dotenv
load_dotenv()

import streamlit as st

# Configure the main page
st.set_page_config(
    page_title="Gemini LLM Hub",
    page_icon="🤖",
    layout="wide",
)

# Main title
st.title("🤖 Gemini LLM Application Hub")
st.markdown("---")

# Welcome section
st.write("""
Welcome to the Gemini LLM Application Hub! This unified application brings together multiple AI-powered tools
powered by Google's Gemini model.

## Available Applications

Navigate through the sidebar to access different applications:

### 📝 Simple Q&A
Ask questions and get instant answers from the Gemini model.

### 💬 Chat Q&A  
Have a multi-turn conversation with the Gemini model while maintaining chat history.

### 👁️ Vision App
Upload images and ask questions about them using Gemini's vision capabilities.

### 🧾 Invoice Extractor
Upload invoice images and extract information using intelligent document analysis.

### 📄 Multi-PDF Chat
Upload multiple PDF documents and ask questions about their content using RAG (Retrieval Augmented Generation).

---

## Technology Stack

- **Framework**: Streamlit
- **LLM**: LangChain + Google Generative AI (Gemini 2.5 Flash)
- **Vector Indexing**: FAISS (for in-memory semantic search in PDF chat)
- **Document Processing**: PyPDF2, Pillow

## Getting Started

1. Select an application from the sidebar
2. Follow the instructions on each page
3. Enjoy AI-powered assistance!

---

**Version**: 2.0 (Multi-page unified app)  
**Last Updated**: March 2026
""")

# Sidebar info
with st.sidebar:
    st.markdown("---")
    st.subheader("About")
    st.info("""
    This application demonstrates various capabilities of the Gemini model:
    - Text understanding and generation
    - Conversational AI
    - Image understanding
    - Document analysis
    - Semantic search and retrieval
    """)