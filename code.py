import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os
import pandas as pd
import io
import re
import time
import concurrent.futures
from google_sheets_exporter import upload_to_google_sheets
from PIL import Image
from io import BytesIO
import base64
import pytesseract  
from PIL import Image
import speech_recognition as sr
from diffusers import StableDiffusionPipeline
import torch

# Configure Streamlit Page
st.set_page_config(page_title="🚀 AI Marketing Generator", layout="wide")

# Load API Keys
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
OPENAI_API_KEY= os.getenv("OPENAI_API_KEY")

# Initialize AI Models
ai_models = {
    "Gemini": ChatGoogleGenerativeAI(model="gemini-1.5-pro", google_api_key=GEMINI_API_KEY),
    "GPT-3.5": ChatOpenAI(model_name="gpt-3.5-turbo", openai_api_key=OPENAI_API_KEY)
}

# Custom CSS
st.markdown("""
<style>
body { font-family: 'Arial', sans-serif; }
.stButton>button { background-color: #4CAF50; color: white; font-size: 16px; }
.st-success { background-color: #e6f7e6; padding: 10px; border-radius: 5px; font-size: 16px; }
.st-warning { background-color: #fff3cd; padding: 10px; border-radius: 5px; }
.st-container { padding: 20px; border-radius: 10px; background-color: #f9f9f9; }
</style>
""", unsafe_allow_html=True)

# Title
st.title("🚀 AI Marketing Generator")
st.write("Generate high-quality marketing slogans, ad copy, and campaign ideas instantly!")

# Session State Init
if "selected_outputs" not in st.session_state:
    st.session_state.selected_outputs = {}
if "last_model" not in st.session_state:
    st.session_state.last_model = "Gemini"


# Optional Input Method Section (Collapsible in Sidebar)
with st.sidebar.expander("🎤🖼️ Optional Input via Image or Voice", expanded=False):
    input_method = st.radio("Choose Input Method", ["None", "Image", "Voice"], horizontal=True)

    if input_method == "Image":
        uploaded_img = st.file_uploader("Upload Image (e.g., logo, product visual)", type=["png", "jpg", "jpeg"])
        if uploaded_img:
            try:
                image = Image.open(BytesIO(uploaded_img.read()))
                st.image(image, caption="Uploaded Image", use_column_width=True)

                extracted_text = pytesseract.image_to_string(image)
                st.success("✅ Text Extracted from Image:")
                st.write(extracted_text)

                # Autofill product name with extracted text
                st.session_state["image_extracted_text"] = extracted_text.strip()
                
            except Exception as e:
                st.error(f"❌ Could not process image: {e}")

    elif input_method == "Voice":
        st.info("🎤 Upload a voice file (WAV format preferred)")
        uploaded_audio = st.file_uploader("Upload Voice File", type=["wav", "mp3", "m4a"])
        if uploaded_audio:
            try:
                recognizer = sr.Recognizer()
                with sr.AudioFile(uploaded_audio) as source:
                    audio_data = recognizer.record(source)
                    voice_text = recognizer.recognize_google(audio_data)
                    st.success("✅ Transcribed Text from Voice:")
                    st.write(voice_text)

                    # Autofill product name with transcribed text
                    st.session_state["image_extracted_text"] = voice_text.strip()
                    
            except Exception as e:
                st.error(f"❌ Could not process audio: {e}")

if st.sidebar.button("🔄 Reset Extracted Input"):
    st.session_state.pop("image_extracted_text", None)
    

# Generate Content

def generate_marketing_content(model, prompt, platform, language):
    if not prompt.strip():
        return ["No output generated. Try again."]

    platform_prompts = {
        "Instagram": "Ensure it's engaging, hashtag-rich, and concise for Instagram.",
        "LinkedIn": "Make it professional, informative, and suitable for business professionals.",
        "Twitter": "Keep it concise, engaging, and within 280 characters with relevant hashtags.",
        "Email": "Make it more personalized, structured, and professional for email marketing.",
        "General": "Generate a general marketing content without platform-specific formatting."
    }

    prompt += f"\n{platform_prompts.get(platform, '')}"
    prompt += f"\nGenerate the content in {language}."

    try:
        response = ai_models[model].invoke(prompt)
        output_text = getattr(response, "content", None)
        if not output_text:
            return ["No output generated. Try again."]
        options = list(set([opt.strip() for opt in output_text.split("\n") if opt.strip()]))
        return options[:5] if options else ["No valid output generated."]
    except Exception as e:
        return [f"Error: {str(e)}"]

# UI Layout
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("🎯 Generate Content for a Single Product")
    category = st.selectbox("Select Content Type", ["Slogan", "Ad Copy", "Campaign Idea"])
    product = st.text_input(
    "Enter Product Name",
    value=st.session_state.get("image_extracted_text", "")
)

    platform = st.selectbox("Select Target Platform", ["General", "Instagram", "LinkedIn", "Twitter", "Email"])
    model_choice = st.selectbox("Choose AI Model", ["Gemini","GPT-3.5"], index=["Gemini","GPT-3.5"].index(st.session_state.last_model))
    tone = st.selectbox("Select Tone", ["Casual", "Professional", "Exciting", "Persuasive"])
    language = st.selectbox("Select Language", ["English","Hindi","Telugu","Tamil","Malayalam", "Spanish", "French", "German", "Chinese", "Japanese"])
    word_limit = st.slider("Word Limit", 10, 100, 50)

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
                output = generate_marketing_content(model_choice, prompt, platform, language)

            if product not in st.session_state.selected_outputs:
                st.session_state.selected_outputs[product] = {}
            st.session_state.selected_outputs[product][category] = {
                "options": output,
                "selected": previous_data["selected"]
            }
            st.session_state.last_model = model_choice
            st.success(f"✅ Content Generated for {product} ({category})")
        else:
            st.warning("⚠️ Please enter a product name before generating content.")

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



@st.cache_resource
def load_sd_model():
    return StableDiffusionPipeline.from_pretrained(
        "CompVis/stable-diffusion-v1-4",
        torch_dtype=torch.float16,
        revision="fp16",
        use_auth_token=None
    ).to("cuda" if torch.cuda.is_available() else "cpu")

pipe = load_sd_model()

# Display Overview & Image Generator
if st.session_state.selected_outputs:
    st.subheader("📌 **Generated Content Overview**")
    for prod, content_dict in st.session_state.selected_outputs.items():
        for content_type, data in content_dict.items():
            options = data["options"]
            selected_option = data["selected"]
            
            st.subheader(f"📌 {content_type} for {prod}")
            st.markdown(f"<div class='st-success'><strong>Selected Content:</strong> {selected_option}</div>", unsafe_allow_html=True)

            with st.expander("🖼️ Generate Image from Selected Text"):
                generate_key = f"generate_image_button_{prod}_{content_type}"
                if st.button("Generate Image", key=generate_key):
                    with st.spinner("Generating image from selected content..."):
                        try:
                            image = pipe(selected_option).images[0]
                            st.image(image, caption=f"Visual for: {selected_option}")
                        except Exception as e:
                            st.error(f"❌ Error generating image: {e}")


# BULK CONTENT GENERATION (UPDATED)
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
                    st.error("❌ You can only enter up to 20 products at a time.")
                else:
                    with st.spinner("Generating content for multiple products..."):
                        def generate_for_product(prod):
                            # ✅ Use platform & language automatically (without showing them)
                            prompt = f"Generate a {category.lower()} for {prod}. Tone: {tone}. Word Limit: {word_limit} words. Platform: {platform}. Language: {language}."
                            return prod, generate_marketing_content(model_choice, prompt, platform, language)

                        # Parallel Processing for Bulk Generation
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
            results.append({"Product": prod, "Content Type": content_type, "Selected Content": selected_option, "Platform": platform, "Word Count": word_count})

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

    # Google Sheet Export Button (for Bulk Results)
    st.markdown("### 📤 Export to Google Sheets")

    if st.button("📤 Export to Google Sheet"):
        success = upload_to_google_sheets(results_df, results_df.columns, sheet_name="Marketing_Content")
        if success:
            st.success("✅ Data uploaded to Google Sheet successfully!")
        else:
            st.error("❌ Failed to upload to Google Sheet. Check credentials and sheet ID.")


