import gspread
import os
from dotenv import load_dotenv
from oauth2client.service_account import ServiceAccountCredentials

# Load environment variables
load_dotenv()

def upload_to_google_sheets(data, columns, sheet_name="Marketing_Content"):
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

    # Read credentials path and Google Sheet details
    creds_path = os.getenv("GOOGLE_SHEET_CREDENTIALS_PATH", "google_credentials.json")  # Default path fallback
    spreadsheet_id = os.getenv("GOOGLE_SHEET_ID")
    sheet_name = os.getenv("GOOGLE_SHEET_NAME", sheet_name)  # Default sheet name

    # Debugging output
    print("🔹 Credentials Path:", creds_path)
    print("🔹 Spreadsheet ID:", spreadsheet_id)
    print("🔹 Sheet Name:", sheet_name)

    if not spreadsheet_id:
        raise ValueError("❌ GOOGLE_SHEET_ID is missing! Check .env file.")

    # Authenticate with Google Sheets
    credentials = ServiceAccountCredentials.from_json_keyfile_name(creds_path, scope)
    client = gspread.authorize(credentials)

    sheet = client.open_by_key(spreadsheet_id)

    try:
        worksheet = sheet.worksheet(sheet_name)
    except gspread.exceptions.WorksheetNotFound:
        print(f"⚠️ Worksheet '{sheet_name}' not found. Creating a new one...")
        worksheet = sheet.add_worksheet(title=sheet_name, rows="1000", cols="20")

    # Debugging Data
    print("🔹 Type of columns:", type(columns))  # Should be <class 'pandas.core.indexes.base.Index'>
    print("🔹 Column Names:", columns)
    print("🔹 Type of data:", type(data))  # Should be list of lists
    print("🔹 First 5 Rows of Data:", data[:5])  # Print first 5 rows

    # Convert columns to a list before adding
    sheet_data = [list(columns)] + data.values.tolist()
  

    # Clear worksheet safely
    try:
        worksheet.clear()
    except Exception as e:
        print(f"⚠️ Warning: Failed to clear worksheet. Error: {e}")

    # Upload Data
    worksheet.update("A1", sheet_data)
    print("✅ Data successfully uploaded to Google Sheets!")

    return True
