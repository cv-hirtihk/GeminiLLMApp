from dotenv import load_dotenv
load_dotenv()

import os
import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage

st.set_page_config(page_title="Chat Q&A", page_icon="💬")
st.header("💬 Chat Q&A with History")
st.write("Have a conversation with the Gemini model while maintaining chat history.")

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

# Initialize session state for chat history if it doesn't exist 
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

# Input
input_text = st.text_input("Enter your question: ", key="input")
submit = st.button("Ask the question")

if submit and input_text:
    with st.spinner("Thinking..."):
        response = get_gemini_response(input_text)
    # Add user query and response to session chat history
    st.session_state['chat_history'].append(("You", input_text))
    st.subheader("Response:")
    st.write(response)
    st.session_state['chat_history'].append(("Gemini", response))

# Display chat history
st.markdown("---")
st.subheader("📜 Chat History")
if st.session_state['chat_history']:
    for role, text in st.session_state['chat_history']:
        if role == "You":
            st.write(f"**You**: {text}")
        else:
            st.write(f"**Gemini**: {text}")
else:
    st.info("No chat history yet. Start by asking a question!")
