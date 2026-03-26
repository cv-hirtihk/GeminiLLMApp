from dotenv import load_dotenv
load_dotenv()

import os
import streamlit as st
from PyPDF2 import PdfReader

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

st.set_page_config(page_title="Multi-PDF Chat", page_icon="📄")
st.header("📄 Chat with Multiple PDFs using Gemini")

# Check if API key is available
if not os.environ.get("GOOGLE_API_KEY"):
    st.warning(
        "🔑 **Please configure your Google Gemini API Key first!**\n\n"
        "Go to the main page and enter your API key in the sidebar configuration section.\n\n"
        "Get your API key from [Google AI Studio](https://aistudio.google.com/app/apikey)"
    )
    st.stop()

# Check if a model is selected
if not st.session_state.get('selected_model'):
    st.error(
        "❌ **No model selected!**\n\n"
        "Please go to the main page and select a model from the sidebar dropdown.\n\n"
        "Make sure your API key is valid and you have access to available models."
    )
    st.stop()

# Get the selected model from session state
model_name = st.session_state.get('selected_model')

FAISS_INDEX_PATH = "faiss_index"
EMBEDDING_MODEL  = "gemini-embedding-001"
LLM_MODEL        = model_name

def get_pdf_text(pdf_docs: list) -> str:
    text = ""
    for pdf in pdf_docs:
        reader = PdfReader(pdf)
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text
    return text

def get_text_chunks(text: str) -> list[str]:
    splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=1000)
    return splitter.split_text(text)

def build_vector_store(text_chunks: list[str]) -> None:
    embeddings = GoogleGenerativeAIEmbeddings(model=EMBEDDING_MODEL)
    vector_store = FAISS.from_texts(text_chunks, embedding=embeddings)
    vector_store.save_local(FAISS_INDEX_PATH)

def load_vector_store() -> FAISS:
    embeddings = GoogleGenerativeAIEmbeddings(model=EMBEDDING_MODEL)
    return FAISS.load_local(FAISS_INDEX_PATH, embeddings=embeddings, allow_dangerous_deserialization=True)

def build_rag_chain(vector_store: FAISS):
    llm = ChatGoogleGenerativeAI(model=LLM_MODEL, temperature=0.3)

    prompt = ChatPromptTemplate.from_messages([
        ("system",
         "Answer the question as detailed as possible using only the context below.\n"
         "If the answer is not in the context, say: "
         "'The answer is not available in the provided documents.'\n"
         "Do not make up answers.\n\n"
         "Context:\n{context}"),
        ("human", "{question}"),
    ])

    retriever = vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 4})

    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    chain = (
        {"context":  retriever | format_docs,
        "question": RunnablePassthrough(),
        } | prompt | llm | StrOutputParser()
    )
    return chain

def user_input(user_question: str) -> None:
    if not os.path.exists(FAISS_INDEX_PATH):
        st.warning("No documents indexed yet. Please upload and process PDFs first.")
        return

    vector_store = load_vector_store()
    chain = build_rag_chain(vector_store)
    result = chain.invoke(user_question)
    st.markdown("**Reply:**")
    st.write(result)

# Main content
st.write("Upload multiple PDF documents and ask questions about their content using Retrieval Augmented Generation (RAG).")

# Input section
user_question = st.text_input("Ask a question about your documents:")
if user_question:
    with st.spinner("Thinking..."):
        user_input(user_question)

# Sidebar for PDF upload
with st.sidebar:
    st.title("📤 Upload PDFs")
    pdf_docs = st.file_uploader("Upload your PDFs", accept_multiple_files=True, type="pdf")
    if st.button("Submit & Process", use_container_width=True):
        if not pdf_docs:
            st.warning("Please upload at least one PDF.")
        else:
            with st.spinner("Processing..."):
                raw_text = get_pdf_text(pdf_docs)
                text_chunks = get_text_chunks(raw_text)
                if not text_chunks:
                    st.error("Could not extract text from the uploaded PDFs.")
                else:
                    build_vector_store(text_chunks)
                    st.success("✅ Done! You can now ask questions about your documents.")
    
    # Check if vector store exists
    if os.path.exists(FAISS_INDEX_PATH):
        st.info("✅ Documents loaded and indexed. You can now ask questions!")
    else:
        st.info("📝 Upload and process PDFs to get started.")
