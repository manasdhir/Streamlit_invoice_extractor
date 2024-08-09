import streamlit as st
import google.generativeai as genai
import os
import tempfile

# Configure API key
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

st.title("Invoice Information Extractor")

uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file is not None:
    # Save the uploaded file to a temporary location
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
        temp_file.write(uploaded_file.read())
        temp_file_path = temp_file.name
    
    # Show spinner while processing
    with st.spinner('Processing...'):
        # Upload file to Google Generative AI
        response = genai.upload_file(path=temp_file_path, display_name="Uploaded Invoice")
        
        # Generate content
        model = genai.GenerativeModel(model_name="models/gemini-1.5-pro-latest")
        result = model.generate_content(["Extract the Customer Details, product details and the Total amount", response])
        
        # Display the result
        st.markdown(f"> {result.text}")
    
    # Delete the temporary file
    os.remove(temp_file_path)
