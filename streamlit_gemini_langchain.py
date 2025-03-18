import streamlit as st 
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os
import pandas as pd
import io

# Load API key
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

# Initialize AI model
llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro", google_api_key=API_KEY)

# Function to generate AI marketing content
def generate_marketing_content(prompt):
    if not prompt.strip():
        return ["No output generated. Try again."]

    try:
        response = llm.invoke(prompt)
        if not response or not getattr(response, "content", None):
            return ["No output generated. Try again."]

        output_text = response.content if isinstance(response.content, str) else str(response)
        options = [opt.strip() for opt in output_text.split("\n") if opt.strip()]

        # Ensure variety in generated options
        options = list(set(options))  # Remove duplicate responses
        while len(options) < 3:
            options.append("⚠️ Placeholder option (AI response incomplete)")

        return options[:3]
    
    except Exception:
        return ["No output generated. Try again."]

# Initialize session state
if "selected_outputs" not in st.session_state:
    st.session_state.selected_outputs = {}

# Streamlit UI
st.set_page_config(page_title="AI Marketing Generator", layout="wide")
st.title("🚀 AI Marketing Generator")
st.write("Generate high-quality marketing slogans, ad copy, and campaign ideas instantly!")

# User Inputs
category = st.selectbox("Select Content Type", ["Slogan", "Ad Copy", "Campaign Idea"])
product = st.text_input("Enter Product Name")

# Single Product Generation
if st.button("🎯 Generate Marketing Content", key="single_product"):
    if product:
        prompt = f"Generate a {category.lower()} for the following product: {product}."
        output = generate_marketing_content(prompt)
        
        st.success(f"✅ Content Generated for {product}")
        for idx, option in enumerate(output):
            st.markdown(f"**Option {idx+1}:** {option}")
    else:
        st.warning("⚠️ Please enter a product name before generating content.")

# File Upload Option
st.write("📂 Upload CSV file with product names")
uploaded_file = st.file_uploader("Drag and drop file here", type=["csv"])

# Bulk Product Generation from CSV
if st.button("🎯 Generate Marketing Content (Bulk)", key="bulk_product"):
    if uploaded_file is None:
        st.warning("⚠️ Please upload a CSV file before generating bulk content.")
    else:
        df = pd.read_csv(uploaded_file)
        if "Product" in df.columns:
            for prod in df["Product"].dropna():
                prompt = f"Generate a {category.lower()} for the following product: {prod}."
                options = generate_marketing_content(prompt)
                st.session_state.selected_outputs[prod] = {"options": options, "selected": None}
        else:
            st.error("CSV file must have a 'Product' column.")

# Display generated options
if st.session_state.selected_outputs:
    results = []
    for prod, data in st.session_state.selected_outputs.items():
        options = data["options"]
        st.subheader(f"📌 **Generated Content for {prod}**")

        for idx, option in enumerate(options):
            st.markdown(f"✅ **Option {idx+1}:** {option}")

        selected_option = st.radio(
            f"Select the best option for {prod}:",
            options,
            index=0,
            key=f"radio_{prod}"
        )
        st.session_state.selected_outputs[prod]["selected"] = selected_option
        
        word_count = len(selected_option.split())
        
        results.append({
            "Product": prod,
            "Selected Content": selected_option,
            "Word Count": word_count
        })

    # Display Results
    if results:
        results_df = pd.DataFrame(results)
        st.subheader("✅ **Selected Marketing Content with Analysis:**")
        st.dataframe(results_df)
        
        # CSV Download
        csv_output = results_df.to_csv(index=False, sep=",", encoding="utf-8")
        st.download_button("📥 Download CSV", csv_output, "selected_marketing_results.csv", "text/csv")

        # Excel Download
        excel_buffer = io.BytesIO()
        with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:
            results_df.to_excel(writer, sheet_name='Results', index=False)
            writer.close()
        st.download_button("📥 Download Excel", excel_buffer.getvalue(), "selected_marketing_results.xlsx", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        
        # Text File Download
        text_output = "\n".join([
            f"Product: {row['Product']}\nContent: {row['Selected Content']}\nWord Count: {row['Word Count']}\n"
            for _, row in results_df.iterrows()
        ])
        st.download_button("📥 Download Text File", text_output.encode('utf-8'), "selected_marketing_results.txt", "text/plain")
        
        # JSON Download
        json_output = results_df.to_json(orient="records", indent=4)
        st.download_button("📥 Download JSON", json_output.encode('utf-8'), "selected_marketing_results.json", "application/json")
