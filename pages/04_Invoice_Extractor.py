from dotenv import load_dotenv
load_dotenv()

import streamlit as st
from PIL import Image
import base64
from io import BytesIO
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage

st.set_page_config(page_title="Invoice Extractor", page_icon="🧾")
st.header("🧾 MultiLanguage Invoice Extractor")
st.write("Upload an invoice image and extract information from it.")

model = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

def pil_to_base64(pil_image):
    """Convert PIL Image to base64 data URL"""
    buffered = BytesIO()
    pil_image.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    return f"data:image/png;base64,{img_str}"

def get_gemini_response(prompt_text, image, user_input):
    # Convert PIL Image to base64 data URL
    image_url = pil_to_base64(image)
    # Combine the prompt, image, and user input into a single message
    message = HumanMessage(
        content=[
            {"type": "text", "text": prompt_text},
            {"type": "text", "text": user_input},
            {"type": "image_url", "image_url": {"url": image_url}},
        ]
    )
    response = model.invoke([message])
    return response.content

input_prompt = """
You are an expert in understanding invoices. 
We will upload an image as invoices and you will have to answer any questions based on the uploaded invoice image.
Be detailed and provide structured information if possible.
"""

# Upload section
st.subheader("Upload Invoice")
uploaded_file = st.file_uploader("Choose an image of the invoice...", type=["jpg", "jpeg", "png"])
image = None
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Invoice", use_column_width=True)

# Question section
st.subheader("Ask Questions")
input_text = st.text_input("Input Prompt: ", key="input")
submit = st.button("Tell me about the invoice")

if submit and image is not None:
    with st.spinner("Analyzing invoice..."):
        response = get_gemini_response(input_prompt, image, input_text)
    st.subheader("Response:")
    st.write(response)
elif submit and image is None:
    st.warning("Please upload an invoice image first.")
