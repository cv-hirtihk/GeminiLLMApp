from dotenv import load_dotenv
load_dotenv() ## loading all env variables

import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage

# function to load Gemini Pro model and get responses
model = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

def get_gemini_response(question):
    response = model.invoke([HumanMessage(content=question)])
    return response.content

# initialize our streamlit app
st.set_page_config(page_title="Q&A Demo")
st.header("Gemini LLM Application")
input = st.text_input("Input: ", key="input")
submit = st.button("Ask the question")

# When submit is clicked
if submit:
    response = get_gemini_response(input)
    st.subheader("The Response is")
    st.write(response)