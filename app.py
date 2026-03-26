from dotenv import load_dotenv
load_dotenv()

import os
import streamlit as st
import requests

# Configure the main page
st.set_page_config(
    page_title="Gemini LLM Hub",
    page_icon="🤖",
    layout="wide",
)

# Function to fetch available models from Google API
@st.cache_data(ttl=3600)
def fetch_available_models(api_key):
    """Fetch available models from Google Generative Language API"""
    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        models_data = response.json()
        models = []
        
        # Extract model names and filter for suitable models
        if 'models' in models_data:
            for model in models_data['models']:
                model_name = model.get('name', '').replace('models/', '')
                # Filter for models that support generation tasks
                supported_generation_methods = model.get('supportedGenerationMethods', [])
                if 'generateContent' in supported_generation_methods and model_name:
                    models.append(model_name)
        
        return sorted(models) if models else None
    except Exception as e:
        st.warning(f"⚠️ Could not fetch models from API: {str(e)}")
        return None

# Sidebar for API Key Configuration
st.sidebar.markdown("## ⚙️ Configuration")
st.sidebar.markdown("---")

# Initialize API key in session state if not present
if 'api_key' not in st.session_state:
    st.session_state.api_key = os.environ.get("GOOGLE_API_KEY", "")

# API Key input field
api_key_input = st.sidebar.text_input(
    "🔑 Enter your Google Gemini API Key:",
    value=st.session_state.api_key,
    type="password",
    help="Your API key is stored only in this session and never saved to disk.",
)

# Update session state if API key changes
if api_key_input:
    st.session_state.api_key = api_key_input
    # Set it as environment variable for the current session
    os.environ["GOOGLE_API_KEY"] = api_key_input
    st.sidebar.success("✅ API Key configured!")
    # Clear cached models when API key changes
    st.cache_data.clear()
elif st.session_state.api_key:
    os.environ["GOOGLE_API_KEY"] = st.session_state.api_key
else:
    st.sidebar.warning("⚠️ No API key detected. Please provide your Google Gemini API Key to use the applications.")

st.sidebar.markdown("---")

# Initialize model in session state if not present
if 'selected_model' not in st.session_state:
    st.session_state.selected_model = None

# Fetch available models if API key is available
api_key = os.environ.get("GOOGLE_API_KEY", "")
if api_key:
    with st.sidebar.spinner("📡 Fetching available models..."):
        available_models = fetch_available_models(api_key)
    
    if available_models:
        # Store available models in session state
        st.session_state.available_models = available_models
        
        # Ensure the current selected model is in the list
        if st.session_state.selected_model not in available_models:
            st.session_state.selected_model = available_models[0]
        
        selected_model = st.sidebar.selectbox(
            "🤖 Select Model:",
            available_models,
            index=available_models.index(st.session_state.selected_model),
            help="Choose which Gemini model to use for the applications.",
        )
        
        # Update session state if model changes
        if selected_model != st.session_state.selected_model:
            st.session_state.selected_model = selected_model
            st.sidebar.info(f"✅ Model changed to: {selected_model}")
    else:
        st.sidebar.error(
            "❌ Could not fetch models from your API key. Please verify:\n"
            "1. Your API key is valid\n"
            "2. Your API key has access to the Generative Language API\n"
            "3. You have internet connectivity"
        )
        st.session_state.selected_model = None
else:
    st.sidebar.info("ℹ️ Enter an API key above to see available models.")

st.sidebar.markdown("---")
st.sidebar.markdown(
    "**Get your API key** from [Google AI Studio](https://aistudio.google.com/app/apikey)"
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