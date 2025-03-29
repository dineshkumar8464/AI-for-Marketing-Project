# from dotenv import load_dotenv
# import os

# load_dotenv()
# api_key = os.getenv("GOOGLE_API_KEY")

# print("Your API Key:", api_key)  # Check if it's loaded properly


import os
from dotenv import load_dotenv

load_dotenv()
print("API Key:", os.getenv("GEMINI_API_KEY"))
print("API Key:", os.getenv("OPENAI_API_KEY"))