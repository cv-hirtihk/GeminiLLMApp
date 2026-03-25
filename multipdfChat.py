from dotenv import load_dotenv
load_dotenv()

import os
import streamlit as st
from PyPDF2 import PdfReader

from langchain_text_splitters import RecursiveCharacterTextSplitter # Cuts large text into smaller chunks
from langchain_community.vectorstores import FAISS # Vector (in-memory) store for storing and querying text chunks using embeddings
from langchain_google_genai import GoogleGenerativeAIEmbeddings # Converts text into numbers (vectors) using Google's model
from langchain_google_genai import ChatGoogleGenerativeAI # The Gemini chat model — the actual AI that answers questions
from langchain_core.prompts import ChatPromptTemplate # A reusable template for structuring prompts for sending to the LLM
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser # Extracts plain text from the AI's response object


FAISS_INDEX_PATH = "faiss_index"
EMBEDDING_MODEL  = "gemini-embedding-001"
LLM_MODEL        = "gemini-2.5-flash"

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
    # the chunk_overlap controls how much content is repeated between consecutive chunks
    splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=1000)
    return splitter.split_text(text)


# Vector store
def build_vector_store(text_chunks: list[str]) -> None:
    embeddings = GoogleGenerativeAIEmbeddings(model=EMBEDDING_MODEL)
    vector_store = FAISS.from_texts(text_chunks, embedding=embeddings)
    vector_store.save_local(FAISS_INDEX_PATH)


def load_vector_store() -> FAISS:
    embeddings = GoogleGenerativeAIEmbeddings(model=EMBEDDING_MODEL)
    return FAISS.load_local(FAISS_INDEX_PATH, embeddings=embeddings, allow_dangerous_deserialization=True)


# RAG Chain
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

    # Converts the FAISS store into a retriever - an object that, given a question, finds the 4 most relevant chunks from your PDFs (k=4).
    retriever = vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 4})

    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    # LangChain Expression Language (LCEL) chain that connects the retriever, prompt, and LLM together.
    # LCEL chain: retrieve → format → prompt → LLM → string output
    chain = (
        {"context":  retriever | format_docs,
        "question": RunnablePassthrough(),
        } | prompt | llm | StrOutputParser()
    )
    return chain


# ── Answer User Question ───────────────────────────────────────────────────────
def user_input(user_question: str) -> None:
    if not os.path.exists(FAISS_INDEX_PATH):
        st.warning("No documents indexed yet. Please upload and process PDFs first.")
        return

    vector_store = load_vector_store()
    chain = build_rag_chain(vector_store)
    result = chain.invoke(user_question) # plain string in, plain string out. It is not tampered
    st.markdown("**Reply:**")
    st.write(result)

def main():
    st.set_page_config(page_title="Chat with Multiple PDFs", page_icon="📄")
    st.header("📄 Chat with Multiple PDFs using Gemini")

    user_question = st.text_input("Ask a question about your documents:")
    if user_question:
        with st.spinner("Thinking..."):
            user_input(user_question)

    with st.sidebar:
        st.title("Menu")
        pdf_docs = st.file_uploader("Upload your PDFs", accept_multiple_files=True, type="pdf",)
        if st.button("Submit & Process"):
            if not pdf_docs:
                st.warning("Please upload at least one PDF.")
                return
            with st.spinner("Processing..."):
                raw_text = get_pdf_text(pdf_docs)
                text_chunks = get_text_chunks(raw_text)
                if not text_chunks:
                    st.error("Could not extract text from the uploaded PDFs.")
                    return
                build_vector_store(text_chunks)
                st.success("Done! You can now ask questions.")


if __name__ == "__main__":
    main()