# Gemini LLM Application Hub

A unified Streamlit multi-page application that brings together multiple AI-powered tools built with LangChain and Google's Generative AI (Gemini models). This application demonstrates various capabilities of Gemini models including text-based Q&A, conversational chatbots, image analysis, document processing, and semantic search with RAG.

## ✨ Features

- **🔑 Dynamic API Key Configuration** - Enter your Google Gemini API key directly through the UI
- **🤖 Dynamic Model Selection** - Automatically fetch and select from available Gemini models via API
- **📝 Simple Q&A** - Ask questions and get instant answers
- **💬 Chat with History** - Multi-turn conversations with maintained context
- **👁️ Vision App** - Upload images and ask questions about them
- **🧾 Invoice Extractor** - Extract information from invoice images
- **📄 Multi-PDF Chat** - RAG-based Q&A across multiple PDF documents
- **🔄 Flexible Model Support** - Works with any available Gemini model from your API key

## 📋 Prerequisites

- Python 3.8 or above
- Google Gemini API Key (get it from [Google AI Studio](https://aistudio.google.com/app/apikey))
- Internet connectivity (for API requests)

## 🚀 Getting Started

### 1. Clone the Repository
```bash
git clone <repository-url>
cd GeminiLLMApp
```

### 2. Create Virtual Environment
```bash
python -m venv venv
```

### 3. Activate Virtual Environment
**Windows:**
```bash
.\venv\Scripts\Activate.ps1
```

**macOS/Linux:**
```bash
source venv/bin/activate
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Run the Application
```bash
streamlit run app.py
```

The application will open in your default web browser at `http://localhost:8501`

## 🔧 Configuration

### API Key Setup
1. Get your API key from [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Launch the application
3. Enter your API key in the sidebar field labeled "🔑 Enter your Google Gemini API Key"
4. The app will automatically fetch available models for your account

### Model Selection
- Once you've entered your API key, available models will be displayed in the "🤖 Select Model" dropdown
- Models are dynamically fetched from your API account
- Switch between models anytime without restarting the app

**Note:** The `.env` file is optional. Your API key is only stored in the current session and never saved to disk.

## 📱 Applications Included

### 1. Simple Q&A (`pages/01_Simple_QA.py`)
Ask any question and get direct answers from your selected Gemini model.

### 2. Chat Q&A (`pages/02_Chat_QA.py`)
Interactive chat interface that maintains conversation history throughout your session.

### 3. Vision App (`pages/03_Vision_App.py`)
Upload images (JPG, JPEG, PNG) and ask questions about them using Gemini's vision capabilities.

### 4. Invoice Extractor (`pages/04_Invoice_Extractor.py`)
Upload invoice images and extract structured information using intelligent vision analysis.

### 5. Multi-PDF Chat (`pages/05_Multi_PDF_Chat.py`)
Upload multiple PDF documents and ask questions about their content using RAG (Retrieval Augmented Generation).

## 📦 Dependencies

* [Streamlit](https://streamlit.io/) - Web framework for building interactive apps
* [LangChain](https://python.langchain.com/) - Framework for building applications with LLMs
* [langchain-google-genai](https://pypi.org/project/langchain-google-genai/) - LangChain integration for Google Generative AI
* [langchain-community](https://pypi.org/project/langchain-community/) - Community integrations for LangChain
* [FAISS](https://github.com/facebookresearch/faiss) - Vector database for semantic search
* [PyPDF2](https://pypi.org/project/PyPDF2/) - PDF parsing and text extraction
* [python-dotenv](https://pypi.org/project/python-dotenv/) - Environment variable management
* [Pillow (PIL)](https://python-pillow.org/) - Image handling and processing
* [requests](https://requests.readthedocs.io/) - HTTP library for API calls

## 🏗️ Architecture

### Multi-Page Structure
```
app.py                          # Main app with configuration sidebar
├── pages/
│   ├── 01_Simple_QA.py        # Simple question answering
│   ├── 02_Chat_QA.py          # Conversational chat with history
│   ├── 03_Vision_App.py       # Image-based Q&A
│   ├── 04_Invoice_Extractor.py # Document extraction
│   └── 05_Multi_PDF_Chat.py   # RAG-based PDF Q&A
└── requirements.txt
```

### Key Features

**Dynamic Configuration:**
- API keys are fetched from the user without requiring `.env` files
- Models are dynamically discovered from the user's API key
- No hardcoded model names - works with any available Gemini model

**Session Management:**
- API key and model selection are stored in Streamlit session state
- Settings persist across page navigation
- Session-based storage ensures security (data cleared on browser close)

**RAG Implementation (Multi-PDF Chat):**
- Uses FAISS for in-memory vector indexing
- Supports semantic search across multiple documents
- Retrieves relevant sections to answer user queries

## 🔐 Security Notes

- **API Keys**: Stored only in the current session, never persisted to disk
- **No Environment Files Required**: `.env` is optional
- **Session-Based**: All user data is cleared when the browser session ends
- **HTTPS**: Always use HTTPS for hosted instances

## 🛠️ Development

### Adding a New Model
The app automatically discovers models from your API key - no code changes needed!

### Troubleshooting

**Models not showing:**
- Verify your API key is valid
- Check that your API key has access to the Generative Language API
- Ensure you have internet connectivity

**Pages show "No model selected":**
- Go back to the main page
- Re-enter your API key to fetch available models
- Select a model from the dropdown

**API Key errors:**
- Double-check your API key from [Google AI Studio](https://aistudio.google.com/app/apikey)
- Ensure the API key is not expired or revoked

## 📝 Version History

**v2.1** (Current)
- Dynamic API key configuration through UI
- Dynamic model selection from available models
- Removed hardcoded model dependencies
- Enhanced security with session-based storage

**v2.0**
- Unified multi-page Streamlit application
- LangChain integration for consistent LLM handling
- RAG support for multi-PDF queries

**v1.0**
- Individual Streamlit applications
- Direct Google SDK integration

## 📄 License

This project is open source and available under the MIT License.

## 🤝 Support

For issues, questions, or suggestions, please open an issue or reach out to the project maintainers.

---

**Last Updated**: March 2026  
**Powered by**: Google Gemini + LangChain + Streamlit