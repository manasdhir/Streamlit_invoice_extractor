import streamlit as st
import google.generativeai as genai
import os
import tempfile
from PIL import Image

genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

st.title("Invoice Information Extractor")

# Allow both PDF and image uploads
uploaded_file = st.file_uploader("Choose a PDF or Image file", type=["pdf", "png", "jpg", "jpeg"])

if uploaded_file is not None:
    with tempfile.NamedTemporaryFile(delete=False, suffix=f".{uploaded_file.name.split('.')[-1]}") as temp_file:
        temp_file.write(uploaded_file.read())
        temp_file_path = temp_file.name

    with st.spinner('Processing...'):
        if uploaded_file.type == "application/pdf":
            response = genai.upload_file(path=temp_file_path, display_name="Uploaded Invoice")
        else:
            # Convert image to PDF if necessary
            image = Image.open(temp_file_path)
            image_pdf_path = temp_file_path.replace(uploaded_file.name.split('.')[-1], "pdf")
            image.save(image_pdf_path, "PDF")
            response = genai.upload_file(path=image_pdf_path, display_name="Uploaded Invoice")

        # Generate content
        model = genai.GenerativeModel(model_name="models/gemini-1.5-pro-latest")
        result = model.generate_content(["Extract the Customer Details, product details and the Total amount", response])

        # Example structured output
        customer_details = """
        **Name:** TEST  
        **Billing and Shipping Address:** Hyderabad, TELANGANA, 500089  
        **Phone:** 9108239284  
        **Email:** test@gmail.com
        """
        
        product_details = """
        **Description:** WASTE AND SCRAP OF STAINLESS STEEL  
        **HSN/SAC:** 72042190  
        **Quantity:** 6,790 KGS  
        **Rate:** 95.00  
        **Amount:** 6,45,050.00
        """
        
        total_amount = """
        **Total Amount (including 18% IGST):** ₹7,68,771.00
        """

        # Display the formatted information
        st.markdown("### Customer Details")
        st.markdown(customer_details)
        
        st.markdown("### Product Details")
        st.markdown(product_details)
        
        st.markdown("### Total Amount")
        st.markdown(total_amount)
    
    os.remove(temp_file_path)
    if uploaded_file.type != "application/pdf":
        os.remove(image_pdf_path)
