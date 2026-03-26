from dotenv import load_dotenv
load_dotenv()

import os
import streamlit as st
from PIL import Image
import base64
from io import BytesIO
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage

st.set_page_config(page_title="Vision App", page_icon="👁️")
st.header("👁️ Gemini Vision App")
st.write("Upload an image and ask questions about it using Gemini's vision capabilities.")

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

def pil_to_base64(pil_image):
    """Convert PIL Image to base64 data URL"""
    buffered = BytesIO()
    pil_image.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    return f"data:image/png;base64,{img_str}"

def get_gemini_response(input_text, image):
    # Convert PIL Image to base64 data URL
    image_url = pil_to_base64(image)
    if input_text != "":
        message = HumanMessage(
            content=[
                {"type": "text", "text": input_text},
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

# Streamlit UI
col1, col2 = st.columns(2)

with col1:
    st.subheader("Upload Image")
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
    image = None
    if uploaded_file is not None:
        image = Image.open(uploaded_file)

with col2:
    st.subheader("Ask Question")
    input_text = st.text_input("Input prompt: ", key="input")

if image is not None:
    st.image(image, caption="Uploaded Image", use_column_width=True)

submit = st.button("Tell me about the image")

# if submit is clicked
if submit and image is not None:
    with st.spinner("Analyzing image..."):
        response = get_gemini_response(input_text, image)
    st.subheader("Response:")
    st.write(response)
