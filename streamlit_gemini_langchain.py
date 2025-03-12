import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI  # Correct Import
from dotenv import load_dotenv
import os

# Load API key from .env file
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

# Initialize LangChain's ChatGoogleGenerativeAI
llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro", google_api_key=API_KEY)

# Function to process and format the AI output
def format_output(text):
    """Refine AI-generated text into a structured format."""
    sections = text.split("**option")  # Split into different options
    formatted_text = ""

    for section in sections:
        if section.strip():
            formatted_text += f"🟢 **Option {section.strip()}**\n\n"  # Highlight each option
    return formatted_text if formatted_text else "No output generated. Try again."

# Function to generate AI content using LangChain
def generate_marketing_content(prompt):
    """Generate marketing content using LangChain's ChatGoogleGenerativeAI."""
    try:
        response = llm.invoke(prompt)  # Use invoke() instead of predict()
        return format_output(response.content)  # Extract text correctly
    except Exception as e:
        return f"❌ Error: {str(e)}"

# Streamlit UI
st.set_page_config(page_title="AI Marketing Generator", layout="wide")
st.title("🚀 AI Marketing Generator")
st.write("Generate high-quality marketing slogans, ad copy, and campaign ideas instantly!")

# User Inputs
category = st.selectbox("Select Content Type", ["Slogan", "Ad Copy", "Campaign Idea"])
tone = st.selectbox("Select Tone", ["Energetic ⚡", "Professional 👔", "Fun 🎉"])
product = st.text_input("Enter Product Name")

if st.button("🎯 Generate Marketing Content"):
    if product:
        prompt = f"Generate a {tone.split()[0].lower()} {category.lower()} for the following product: {product}."
        output = generate_marketing_content(prompt)
        
        st.success("✅ Content Generated Successfully!")
        st.subheader("📌 **Generated Content**:")
        st.markdown(output, unsafe_allow_html=True)
    else:
        st.warning("⚠️ Please enter a product description.")
