import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os
import pandas as pd
import io
import re
import time
import concurrent.futures  # For parallel processing

# Configure Streamlit Page
st.set_page_config(page_title="🚀 AI Marketing Generator", layout="wide")

# Load API Keys
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Initialize AI Models
ai_models = {
    "Gemini": ChatGoogleGenerativeAI(model="gemini-1.5-pro", google_api_key=GEMINI_API_KEY),
    "GPT-3.5": ChatOpenAI(model_name="gpt-3.5-turbo", openai_api_key=OPENAI_API_KEY)
}

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

# Initialize Session State for Content Persistence
if "selected_outputs" not in st.session_state:
    st.session_state.selected_outputs = {}

if "last_model" not in st.session_state:
    st.session_state.last_model = "Gemini"  # Default model

# AI Function: Generate Marketing Content
def generate_marketing_content(model, prompt):
    """Generates marketing content using the selected AI model."""
    if not prompt.strip():
        return ["No output generated. Try again."]
    
    try:
        response = ai_models[model].invoke(prompt)
        output_text = getattr(response, "content", None)

        if not output_text:
            return ["No output generated. Try again."]

        options = list(set([opt.strip() for opt in output_text.split("\n") if opt.strip()]))
        return options[:5] if options else ["No valid output generated."]
    except Exception as e:
        return [f"Error: {str(e)}"]

# UI Layout with Columns
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("🎯 Generate Content for a Single Product")
    
    category = st.selectbox("Select Content Type", ["Slogan", "Ad Copy", "Campaign Idea"])
    product = st.text_input("Enter Product Name")
    model_choice = st.selectbox("Choose AI Model", list(ai_models.keys()), index=list(ai_models.keys()).index(st.session_state.last_model))
    tone = st.selectbox("Select Tone", ["Casual", "Professional", "Exciting", "Persuasive"])
    word_limit = st.slider("Word Limit", 10, 100, 50)

    # Preserve previously generated content when switching models
    if product and category in st.session_state.selected_outputs.get(product, {}):
        previous_data = st.session_state.selected_outputs[product][category]
    else:
        previous_data = {"options": [], "selected": ""}

    if st.button("Generate Marketing Content", key="single_product"):
        if product:
            with st.spinner("Generating content..."):
                prompt = f"""
                Generate structured {category.lower()} variations for {product}.
                Tone: {tone}.
                Word Limit: {word_limit} words.
                Include SEO keywords relevant to the product.
                Provide multiple creative variations.
                """
                output = generate_marketing_content(model_choice, prompt)

            # Store in session state to preserve content when switching models
            if product not in st.session_state.selected_outputs:
                st.session_state.selected_outputs[product] = {}

            st.session_state.selected_outputs[product][category] = {
                "options": output,
                "selected": previous_data["selected"]
            }

            st.session_state.last_model = model_choice  # Update last used model
            st.success(f"✅ Content Generated for {product} ({category})")
        else:
            st.warning("⚠️ Please enter a product name before generating content.")

    # Display All Generated Content for the Product
    if product in st.session_state.selected_outputs:
        for content_type, data in st.session_state.selected_outputs[product].items():
            st.subheader(f"🔹 {content_type} for {product}")
            selected_option = st.radio(
                f"Select the best {content_type}:",
                data["options"] if data["options"] else ["No content generated yet."],
                index=0 if data["options"] else None,
                key=f"radio_{product}_{content_type}"
            )
            st.session_state.selected_outputs[product][content_type]["selected"] = selected_option

            st.markdown(f"<div class='st-success'><strong>Selected Content ({content_type}):</strong> {selected_option}</div>", unsafe_allow_html=True)

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

                if len(products) > 20:
                    st.error("❌ You can only enter up to 20 products at a time. Please reduce your input.")
                else:
                    with st.spinner("Generating content for multiple products..."):
                        def generate_for_product(prod):
                            prompt = f"Generate a {category.lower()} for {prod}. Tone: {tone}. Word Limit: {word_limit} words."
                            return prod, generate_marketing_content(model_choice, prompt)

                        # Use parallel processing for efficiency
                        with concurrent.futures.ThreadPoolExecutor() as executor:
                            results = executor.map(generate_for_product, products)

                        for prod, options in results:
                            if prod not in st.session_state.selected_outputs:
                                st.session_state.selected_outputs[prod] = {}

                            st.session_state.selected_outputs[prod][category] = {"options": options, "selected": ""}

                    st.session_state.last_model = model_choice  # Preserve last model used
            else:
                st.error("❌ CSV file must have a 'Product' column.")

# Display Bulk Generated Options
if st.session_state.selected_outputs:
    st.subheader("📌 **Generated Content Overview**")
    results = []
    
    for prod, content_dict in st.session_state.selected_outputs.items():
        for content_type, data in content_dict.items():
            options = data["options"]
            selected_option = data["selected"]

            st.subheader(f"📌 **{content_type} for {prod}**")
            selected_option = st.radio(f"Select the best {content_type} for {prod}:", options, index=0, key=f"radio_{prod}_{content_type}_bulk")
            st.session_state.selected_outputs[prod][content_type]["selected"] = selected_option

            st.markdown(f"<div class='st-success'><strong>Selected Content:</strong> {selected_option}</div>", unsafe_allow_html=True)

            word_count = len(re.findall(r'\b\w+\b', selected_option))
            results.append({"Product": prod, "Content Type": content_type, "Selected Content": selected_option, "Word Count": word_count})
    
    results_df = pd.DataFrame(results)
    st.dataframe(results_df)
    
    csv_output = results_df.to_csv(index=False)
    st.download_button("📥 Download CSV", csv_output, "marketing_results.csv", "text/csv")
    
    excel_buffer = io.BytesIO()
    with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:
        results_df.to_excel(writer, sheet_name='Results', index=False)
    st.download_button("📥 Download Excel", excel_buffer.getvalue(), "marketing_results.xlsx", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

    text_output = "\n".join([f"Product: {row['Product']}\nContent Type: {row['Content Type']}\nContent: {row['Selected Content']}\nWord Count: {row['Word Count']}\n" for _, row in results_df.iterrows()])
    st.download_button("📥 Download Text File", text_output.encode('utf-8'), "selected_marketing_results.txt", "text/plain")
    
    json_output = results_df.to_json(orient="records", indent=4)
    st.download_button("📥 Download JSON", json_output.encode('utf-8'), "selected_marketing_results.json", "application/json")
