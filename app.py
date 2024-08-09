import streamlit as st
import google.generativeai as genai
import os
import tempfile
from PIL import Image

genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

st.title("Invoice Information Extractor")

uploaded_file = st.file_uploader("Choose a PDF or Image file", type=["pdf", "png", "jpg", "jpeg"])

if uploaded_file is not None:
    with tempfile.NamedTemporaryFile(delete=False, suffix=f".{uploaded_file.name.split('.')[-1]}") as temp_file:
        temp_file.write(uploaded_file.read())
        temp_file_path = temp_file.name

    with st.spinner('Processing...'):
        if uploaded_file.type == "application/pdf":
            response = genai.upload_file(path=temp_file_path, display_name="Uploaded Invoice")
        else:
            image = Image.open(temp_file_path)
            image_pdf_path = temp_file_path.replace(uploaded_file.name.split('.')[-1], "pdf")
            image.save(image_pdf_path, "PDF")
            response = genai.upload_file(path=image_pdf_path, display_name="Uploaded Invoice")

        model = genai.GenerativeModel(model_name="models/gemini-1.5-pro-latest")
        prompt = (
            "Extract the Customer Details, Product Details, and the Total Amount from this invoice. "
            "Please format the information in markdown with headings for each section and bullet points for details."
        )
        result = model.generate_content([prompt, response])

        st.markdown(result.text)

    os.remove(temp_file_path)
    if uploaded_file.type != "application/pdf":
        os.remove(image_pdf_path)

