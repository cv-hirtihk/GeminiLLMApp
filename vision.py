from dotenv import load_dotenv
load_dotenv() ## loading all env variables

import streamlit as st
from PIL import Image
import base64
from io import BytesIO
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage

## funtion to load Gemini Pro model and get responses
model = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

def pil_to_base64(pil_image):
    """Convert PIL Image to base64 data URL"""
    buffered = BytesIO()
    pil_image.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    return f"data:image/png;base64,{img_str}"

def get_gemini_response(input, image):
    # Convert PIL Image to base64 data URL
    image_url = pil_to_base64(image)
    if input != "":
        message = HumanMessage(
            content=[
                {"type": "text", "text": input},
                {"type": "image_url", "image_url": {"url": image_url}},
            ]
        )
    else:
        message = HumanMessage(
            content=[
                {"type": "image_url", "image_url": {"url": image_url}},
            ]
        )
    response = model.invoke([message])
    return response.content

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