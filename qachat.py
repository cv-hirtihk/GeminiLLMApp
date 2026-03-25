from dotenv import load_dotenv
load_dotenv() ## loading all env variables

import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage

## funtion to load Gemini Pro model and get responses
model = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

def get_gemini_response(question):
    response = model.invoke([HumanMessage(content=question)])
    return response.content

st.set_page_config(page_title="Q&A Demo")

st.header("Gemini LLM Application")

# Initialize session state for chat history if it doesn't exist 
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

input = st.text_input("Input: ", key="input")
submit = st.button("Ask the question")

if submit and input:
    response = get_gemini_response(input)
    # Add user query and response to session chat history
    st.session_state['chat_history'].append(("You", input))
    st.subheader("The Response is")
    st.write(response)
    st.session_state['chat_history'].append(("LLM", response))

st.subheader("The chat history is")
for role, text in st.session_state['chat_history']:
    st.write(f"{role}: {text}")
