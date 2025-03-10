from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

print("Your API Key:", api_key)  # Check if it's loaded properly
