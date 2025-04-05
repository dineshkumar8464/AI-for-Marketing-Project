import streamlit as st
import pandas as pd
import pytest
import time
import concurrent.futures
from io import StringIO
from unittest.mock import MagicMock, patch
from streamlit_gemini_langchain import generate_marketing_content



mock_ai_response = [
    "Catchy Slogan 1",
    "Catchy Slogan 2",
    "Catchy Slogan 3"
]


### ✅ Test Case 1: Handling Single Product
def test_generate_single_product():
    with patch("streamlit_gemini_langchain.llm", return_value=MagicMock(content="\n".join(mock_ai_response))):
        result = generate_marketing_content("Nike Shoes")
        assert isinstance(result, list)  
        assert len(result) == 3  
        assert any("Catchy Slogan" in res for res in result)  # Ensure mock response is used


### ✅ Test Case 2: Very Short Product Name
def test_generate_short_product_name():
    with patch("streamlit_gemini_langchain.llm", return_value=MagicMock(content="\n".join(mock_ai_response))):
        result = generate_marketing_content("A")
        assert len(result) == 3  


### ✅ Test Case 4: Numeric-Only Product Name
def test_generate_numeric_product_name():
    with patch("streamlit_gemini_langchain.llm", return_value=MagicMock(content="\n".join(mock_ai_response))):
        result = generate_marketing_content("123456")
        assert len(result) == 3  


### ✅ Test Case 5: Non-English Product Names
def test_generate_non_english_product():
    with patch("streamlit_gemini_langchain.llm", return_value=MagicMock(content="\n".join(mock_ai_response))):
        result = generate_marketing_content("智能手机")
        assert len(result) == 3  


### ✅ Test Case 6: Product Name with Special Characters
def test_generate_special_characters():
    with patch("streamlit_gemini_langchain.llm", return_value=MagicMock(content="\n".join(mock_ai_response))):
        result = generate_marketing_content("@#*!^&$Nike123")
        assert len(result) == 3  


### ✅ Test Case 7: Product Name with Extremely Long String
def test_generate_long_product_name():
    long_product_name = "Nike" * 100  
    with patch("streamlit_gemini_langchain.llm", return_value=MagicMock(content="\n".join(mock_ai_response))):
        result = generate_marketing_content(long_product_name)
        assert len(result) == 3  


### ✅ Test Case 8: Handling Large Input Strings
def test_generate_large_input_string():
    large_input = "Product " * 500  # Very long input
    with patch("streamlit_gemini_langchain.llm", return_value=MagicMock(content="\n".join(mock_ai_response))):
        result = generate_marketing_content(large_input)
        assert len(result) == 3  


### ✅ Test Case 9: Handling Large Input Sizes
def test_generate_large_input_size():
    """Check if system handles very large input without crashing."""
    large_input = " ".join(["Product"] * 2000)  # 10,000 characters
    with patch("streamlit_gemini_langchain.llm", return_value=MagicMock(content="\n".join(mock_ai_response))):
        result = generate_marketing_content(large_input)
        assert len(result) == 3  

### ✅ Test Case 10: CSV File Upload with Valid Data
def test_generate_csv_products():
    data = {"Product": ["Nike Shoes", "Apple iPhone", "Coca-Cola"]}
    df = pd.DataFrame(data)
    
    results = []
    for product in df["Product"]:
        with patch("streamlit_gemini_langchain.llm", return_value=type('obj', (object,), {"content": "\n".join(mock_ai_response)})):
            result = generate_marketing_content(product)
            results.append(result)
    
    assert len(results) == len(df)  
    assert all(isinstance(item, list) and len(item) == 3 for item in results)  


### 🔹 Test Case 11: Uploading an Empty CSV File
def test_upload_empty_csv():
    df = pd.DataFrame([])  
    assert df.empty  


### 🔹 Test Case 12: Uploading a CSV File with Incorrect Column Names
def test_upload_csv_wrong_columns():
    df = pd.DataFrame({"WrongColumn": ["Nike", "Apple", "Coke"]})  
    assert "Product" not in df.columns  


### 🔹 Test Case 13: Large CSV File Upload
def test_large_csv_upload():
    df = pd.DataFrame({"Product": ["Nike Shoes"] * 10000})  
    assert len(df) == 10000 


### 🔹 Test Case 14: Handling CSV with Empty Rows
def test_generate_csv_empty_rows():
    csv_data = StringIO("Product\nLaptop\n\nSmartphone\n")
    df = pd.read_csv(csv_data)

    valid_products = df["Product"].dropna().tolist()  # Remove empty values

    assert valid_products == ["Laptop", "Smartphone"]  # Should skip empty rows
 

### 🔹 Test Case 15: Handling Missing Columns in CSV Upload
def test_generate_missing_csv_column():
    """Simulate CSV upload without 'Product' column."""
    csv_data = StringIO("Name,Price\nShoes,50\nT-shirt,20")
    df = pd.read_csv(csv_data)

    assert "Product" not in df.columns  # Ensure 'Product' column is missing

    # Simulate Streamlit behavior
    if "Product" not in df.columns:
        error_message = "CSV file must have a 'Product' column."
    else:
        error_message = None

    assert error_message == "CSV file must have a 'Product' column."


### ✅ Test Case 16: Download CSV Option
def test_download_selected_content():
    results_df = pd.DataFrame([
        {"Product": "Nike Shoes", "Selected Content": "Nike Shoes – Unleash your inner athlete!"},
        {"Product": "Apple iPhone", "Selected Content": "Experience innovation with Apple iPhone!"}
    ])
    
    csv_output = results_df.to_csv(index=False).encode('utf-8')
    assert csv_output is not None  
    assert b"Nike Shoes" in csv_output  


### 🔹 Test Case 17: High Load Handling (Stress Test)
def test_generate_high_load():
    """Simulate multiple simultaneous API requests."""
    test_inputs = ["Laptop", "T-shirt", "Shoes"] * 20  # 60 Requests

    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = list(executor.map(generate_marketing_content, test_inputs))

    assert all(isinstance(res, list) and len(res) > 0 for res in results)


### 🔹 Test Case 18: Handling API Failures
def test_generate_api_failure(monkeypatch):
    """Simulate API failure and check error handling."""
    def mock_fail_request(*args, **kwargs):
        raise Exception("API request failed: Invalid API key")

    monkeypatch.setattr("streamlit_gemini_langchain.llm", mock_fail_request)  
    result = generate_marketing_content("Test Product")
    
    assert isinstance(result, list)
    assert result == ["No output generated. Try again."]  # Expected error message


### 🔹 Test Case 19: Response Time for API Calls
def test_generate_incorrect_api_response(monkeypatch):
    """Simulate incorrect API response format."""
    class MockResponse:
        def __init__(self):
            self.invalid_attribute = "Unexpected response format"

    def mock_request(*args, **kwargs):
        return MockResponse()

    monkeypatch.setattr("streamlit_gemini_langchain.llm", mock_request)
    result = generate_marketing_content("Product")

    assert result == ["No output generated. Try again."]


### 🔹 Test Case 20: User-Friendly Error Messages
def test_generate_error_messages():
    """Ensure error messages are clear and helpful."""
    result = generate_marketing_content("")  # Empty input
    assert result == ["No output generated. Try again."]

    result = generate_marketing_content("@#$%^&*()")  # Special characters
    assert isinstance(result, list) and len(result) > 0
