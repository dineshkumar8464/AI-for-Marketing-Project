import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os
import pandas as pd
import io
import re
import time 


# Configure Streamlit Page
st.set_page_config(page_title="🚀 AI Marketing Generator", layout="wide")

# Load API Key
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

# Initialize AI Model
llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro", google_api_key=API_KEY)

# Custom CSS for UI Enhancements
st.markdown(
    """
    <style>
    body { font-family: 'Arial', sans-serif; }
    .stButton>button { background-color: #4CAF50; color: white; font-size: 16px; }
    .st-success { background-color: #e6f7e6; padding: 10px; border-radius: 5px; font-size: 16px; }
    .st-warning { background-color: #fff3cd; padding: 10px; border-radius: 5px; }
    .st-container { padding: 20px; border-radius: 10px; background-color: #f9f9f9; }
    </style>
    """,
    unsafe_allow_html=True
)

# Title and Introduction
st.title("🚀 AI Marketing Generator")
st.write("Generate high-quality marketing slogans, ad copy, and campaign ideas instantly!")

# AI Function: Generate Marketing Content
def generate_marketing_content(prompt):
    if not prompt.strip():
        return ["No output generated. Try again."]
    
    try:
        response = llm.invoke(prompt)
        if not response or not getattr(response, "content", None):
            return ["No output generated. Try again."]
        
        output_text = response.content if isinstance(response.content, str) else str(response)
        options = list(set([opt.strip() for opt in output_text.split("\n") if opt.strip()]))
        return options[:5] if options else ["No valid output generated."]
    except Exception:
        return ["No output generated. Try again."]

# Session State
if "selected_outputs" not in st.session_state:
    st.session_state.selected_outputs = {}

# UI Layout with Columns
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("🎯 Generate Content for a Single Product")
    category = st.selectbox("Select Content Type", ["Slogan", "Ad Copy", "Campaign Idea"])
    product = st.text_input("Enter Product Name")

    if st.button("Generate Marketing Content", key="single_product"):
        if product:
            with st.spinner("Generating content..."):
                prompt = f"Generate multiple structured {category.lower()} variations for: {product}."
                output = generate_marketing_content(prompt)
            
            st.session_state.selected_outputs[product] = {
                "options": output,
                "selected": st.session_state.selected_outputs.get(product, {}).get("selected", "")
            }
            
            st.success(f"✅ Content Generated for {product}")
        else:
            st.warning("⚠️ Please enter a product name before generating content.")

    # Display Generated Content
    if product in st.session_state.selected_outputs:
        output = st.session_state.selected_outputs[product]["options"]
        selected_option = st.session_state.selected_outputs[product]["selected"]
        
        st.subheader("🔹 Choose the best one:")
        selected_option = st.radio("Select the best option:", output, index=0, key=f"radio_{product}")
        st.session_state.selected_outputs[product]["selected"] = selected_option
        
        st.markdown(f"<div class='st-success'><strong>Selected Content:</strong> {selected_option}</div>", unsafe_allow_html=True)

with col2:
    st.subheader("📂 Bulk Content Generation")
    uploaded_file = st.file_uploader("Upload CSV file with product names", type=["csv"])
    
    if st.button("Generate Marketing Content (Bulk)", key="bulk_product"):
        if uploaded_file is None:
            st.warning("⚠️ Please upload a CSV file before generating bulk content.")
        else:
            df = pd.read_csv(uploaded_file)
            
            if "Product" in df.columns:
                products = df["Product"].dropna().tolist()
                
                # **Check if product count exceeds 20**
                if len(products) > 20:
                    st.error("❌ You can only enter up to 20 products at a time. Please reduce your input.")
                else:
                    with st.spinner("Generating content for multiple products..."):
                        for prod in products:
                            prompt = f"Generate a {category.lower()} for the following product: {prod}."
                            options = generate_marketing_content(prompt)

                            # Store output in session state
                            st.session_state.selected_outputs[prod] = {"options": options, "selected": ""}

                            time.sleep(2)  # Add delay to prevent API rate limiting
            else:
                st.error("❌ CSV file must have a 'Product' column.")

# Display Bulk Generated Options
if st.session_state.selected_outputs:
    st.subheader("📌 **Generated Content Overview**")
    results = []
    
    for prod, data in st.session_state.selected_outputs.items():
        options = data["options"]
        selected_option = data["selected"]
        
        st.subheader(f"📌 **{prod}**")
        selected_option = st.radio(f"Select the best option for {prod}:", options, index=0, key=f"radio_{prod}_bulk")
        st.session_state.selected_outputs[prod]["selected"] = selected_option
        
        st.markdown(f"<div class='st-success'><strong>Selected Content:</strong> {selected_option}</div>", unsafe_allow_html=True)
        
        
        word_count = len(re.findall(r'\b\w+\b', selected_option))
        results.append({"Product": prod, "Selected Content": selected_option, "Word Count": word_count})
    
    results_df = pd.DataFrame(results)
    st.dataframe(results_df)
    
    csv_output = results_df.to_csv(index=False)
    st.download_button("📥 Download CSV", csv_output, "marketing_results.csv", "text/csv")
    
    excel_buffer = io.BytesIO()
    with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:
        results_df.to_excel(writer, sheet_name='Results', index=False)
    st.download_button("📥 Download Excel", excel_buffer.getvalue(), "marketing_results.xlsx", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

    # Text File Download
    text_output = "\n".join([
        f"Product: {row['Product']}\nContent: {row['Selected Content']}\nWord Count: {row['Word Count']}\n"
        for _, row in results_df.iterrows()
    ])
    st.download_button("📥 Download Text File", text_output.encode('utf-8'), "selected_marketing_results.txt", "text/plain")
    
    # JSON Download
    json_output = results_df.to_json(orient="records", indent=4)
    st.download_button("📥 Download JSON", json_output.encode('utf-8'), "selected_marketing_results.json", "application/json")