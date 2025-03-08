import streamlit as st
import google.generativeai as genai

# Configure Gemini API key
genai.configure(api_key="AIzaSyCw0thuMOlJ2mWD5FcepTVJf5SxPF4m46M")

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
st.title("AI Marketing Generator")
st.write("Generate high-quality marketing slogans, ad copy, and campaign ideas instantly!")

# User input
category = st.selectbox("Select Content Type", ["Slogan", "Ad Copy", "Campaign Idea"])
product = st.text_input("Enter Product Name")

generate_button = st.button("Generate Marketing Content")

if generate_button:
    if product:
        prompt = f"Generate a creative {category.lower()} for a product called '{product}'."
        output = generate_marketing_content(prompt)
        st.subheader(f"Generated {category}:")
        st.write(output)
    else:
        st.warning("Please enter a product name.")