from dotenv import load_dotenv
load_dotenv() ## loading all env variables

import streamlit as st
import os
from PIL import Image
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

## funtion to load Gemini Pro model and get responses
model = genai.GenerativeModel("gemini-2.5-flash")
def get_gemini_response(input, image):
    if input != "":
        response = model.generate_content([input, image])
    else:
        response = model.generate_content(image)
    return response.text

## Streamlit UI
st.set_page_config(page_title="Gemini Vision")
st.header("Gemini Vision App")

input = st.text_input("Input prompt: ", key="input")
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
image = ""
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

submit = st.button("Tell me about the image")

#if submit is clicked
if submit:
    response = get_gemini_response(input, image)
    st.subheader("The Response is")
    st.write(response)