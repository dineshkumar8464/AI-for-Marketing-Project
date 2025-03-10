import streamlitcode as st
from langchain_google_genai import ChatGoogleGenerativeAI
import os

# Set API key
os.environ["GOOGLE_API_KEY"] = "AIzaSyA2WApH-qFk1hetH3wmpT1pR6J0OOm3U3c"

# Initialize LangChain model
llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro")

# Streamlit UI
st.title("AI-Powered Marketing Content Generator")
st.write("Generate **slogans, ad copies, or campaign ideas** instantly!")

# User input fields
content_type = st.radio("What do you need?", ["Slogan", "Ad Copy", "Campaign Idea"])
user_input = st.text_area("Describe your product/service:", "")

if st.button("Generate"):
    if user_input:
        # Craft the right prompt for the AI
        prompt = f"Generate a {content_type.lower()} for: {user_input}"
        response = llm.invoke(prompt)
        
        # Display response
        st.subheader(f"AI-Generated {content_type}:")
        st.write(response.content)
    else:
        st.warning("Please enter a product or service description.")

