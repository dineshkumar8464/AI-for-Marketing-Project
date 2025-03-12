import streamlit as st
import google.generativeai as genai

# Configure Gemini API key
genai.configure(api_key="AIzaSyA2WApH-qFk1hetH3wmpT1pR6J0OOm3U3c")

# Define model configuration
generation_config = {
    "temperature": 0.3,  # Lower value for more accurate responses
    "max_output_tokens": 100,  # Limit response length
    "top_p": 0.9,  # Helps refine randomness
}

# Function to generate marketing content
def generate_marketing_content(prompt, model="gemini-1.5-pro"):
    """Generate marketing content using Gemini API with proper parameter tuning."""
    try:
        gen_model = genai.GenerativeModel(model, generation_config=generation_config)
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

if st.button("Generate Marketing Content"):
    if product:
        prompt = f"Generate a creative {category.lower()} for a product called '{product}'."
        output = generate_marketing_content(prompt)
        st.subheader(f"Generated {category}:")
        st.write(output)
    else:
        st.warning("Please enter a product name.")
