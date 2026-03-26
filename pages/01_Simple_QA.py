from dotenv import load_dotenv
load_dotenv()

import os
import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage

st.set_page_config(page_title="Simple Q&A", page_icon="📝")
st.header("📝 Simple Q&A")
st.write("Ask any question and get instant answers from the Gemini model.")

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
model = ChatGoogleGenerativeAI(model=model_name)

def get_gemini_response(question):
    response = model.invoke([HumanMessage(content=question)])
    return response.content

# Input
input_text = st.text_input("Enter your question: ", key="input")
submit = st.button("Ask the question")

# When submit is clicked
if submit and input_text:
    with st.spinner("Thinking..."):
        response = get_gemini_response(input_text)
    st.subheader("Response:")
    st.write(response)
