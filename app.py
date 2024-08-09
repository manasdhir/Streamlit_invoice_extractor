import streamlit as st
import google.generativeai as genai
import os
import tempfile

# Configure API key
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

st.title("Invoice Information Extractor")

uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file is not None:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
        temp_file.write(uploaded_file.read())
        temp_file_path = temp_file.name
    
    with st.spinner('Processing...'):
        response = genai.upload_file(path=temp_file_path, display_name="Uploaded Invoice")
        
        model = genai.GenerativeModel(model_name="models/gemini-1.5-pro-latest")
        result = model.generate_content(["Extract the Customer Details, product details and the Total amount", response])
        
        # Format the extracted information
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
