from dotenv import load_dotenv
load_dotenv()

import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage

st.set_page_config(page_title="Simple Q&A", page_icon="📝")
st.header("📝 Simple Q&A")
st.write("Ask any question and get instant answers from the Gemini model.")

# function to load Gemini Pro model and get responses
model = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

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
