import streamlit as st
import google.generativeai as genai
from PIL import Image
import time

# Configure Gemini API key
genai.configure(api_key="AIzaSyA2WApH-qFk1hetH3wmpT1pR6J0OOm3U3c")

def generate_marketing_content(prompt, model="models/gemini-1.5-pro"):
    """Generate marketing content using Gemini API."""
    try:
        gen_model = genai.GenerativeModel(model)
        response = gen_model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"

# Streamlit UI
st.set_page_config(page_title="AI Marketing Generator", layout="wide")

# Custom Styling
st.markdown(
    """
    <style>
        body {
            background-color: #f8f9fa;
        }
        .main-title {
            font-size: 36px;
            font-weight: bold;
            text-align: center;
            color: #333;
        }
        .sub-text {
            text-align: center;
            font-size: 18px;
            color: #555;
        }
        .stTextInput, .stSelectbox, .stButton {
            margin-top: 20px;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# Page Title
st.markdown("<div class='main-title'>AI Marketing Generator</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-text'>Generate high-quality marketing slogans, ad copy, and campaign ideas instantly!</div>", unsafe_allow_html=True)

# User Input Section
st.write("### Select Options")
category = st.selectbox("Select Content Type", ["Slogan", "Ad Copy", "Campaign Idea"], index=2)
product = st.text_input("Enter Product Name", placeholder="e.g., Nike Shoes")

generate_button = st.button("Generate Marketing Content")

if generate_button:
    if product:
        with st.spinner("Generating content... Please wait"):
            time.sleep(2)  # Simulating a delay for a better user experience
            prompt = f"Generate a creative {category.lower()} for a product called '{product}'."
            output = generate_marketing_content(prompt)
            
            st.success("Content Generated Successfully!")
            st.write("### Generated Content:")
            st.info(output)
    else:
        st.warning("⚠️ Please enter a product name.")
