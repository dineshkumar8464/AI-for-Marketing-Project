import os
from dotenv import load_dotenv

load_dotenv()
print("API Key:", os.getenv("GEMINI_API_KEY"))
print("API Key:", os.getenv("OPENAI_API_KEY"))
print("API Key:", os.getenv("GOOGLE_SHEET_API_KEY"))
print("Sheet ID:", os.getenv("GOOGLE_SHEET_ID"))
print("Sheet Credentials path:", os.getenv("GOOGLE_SHEET_CREDENTIALS_PATH"))
print("sheet name:", os.getenv("GOOGLE_SHEET_NAME"))
