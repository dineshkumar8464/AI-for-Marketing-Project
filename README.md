## 📄 Full Report  
You can download the full documentation [here](https://github.com/dineshkumar8464/AI-for-Marketing-Project/blob/master/AI_FOR_MARKETING_REPORT.pdf).


**Overview**:

🧠 AI Marketing Content Generator
This AI Marketing Content Generator is a Streamlit-based web application that leverages the power of Gemini Pro (gemini-2.5-pro-exp-03-25) and OpenAI GPT-3.5 models to help marketers and creators generate high-quality marketing content quickly and efficiently. With support for both single and bulk generation, the app offers a seamless experience for content creation and export.


**🔧 Features:**

✨ Single Content Generation: Instantly generate engaging marketing content using either Gemini Pro or OpenAI models.

📂 Bulk Content Generation: Upload an Excel file and generate content for multiple entries of 20 productsms at once.

📤 Export Options: Download your content as .csv, .json, .txt, or even export directly to Google Sheets.

🎨 AI Image Generation: Powered by Stable Diffusion, convert selected content into stunning visuals.

🖼️ Image-to-Text Input (Coming Soon): Upload an image and extract text to generate content from it.

🎙️ Voice-to-Text Input (Coming Soon): Speak your ideas and let the app generate marketing content from your voice input.

🎨 User Interface (UI): Designed with Stream lit, providing an intuitive and user-friendly experience.

🤖 AI Model Integration (Gemini & GPT-3.5):	Incorporates Google Gemini Pro (🧠 gemini-2.5-pro-exp-03-25) and OpenAI’s GPT-3.5 Turbo for content generation. Users can switch btw models to compare outputs.

🎯 Content Customization: Users can adjust tone (💬 Casual, 🧑‍💼 Professional, ⚡ Exciting, 🛍️ Persuasive), choose platform (📄 General, 📸 Instagram, 📘 Facebook, ✉️ Gmail, 🐦 Twitter), set word limit & SEO, and select language (🇬🇧 English, 🇮🇳 Telugu, 🇮🇳 Hindi, 🇮🇳 Tamil, 🇮🇳 Malayalam, 🇪🇸 Spanish, 🇫🇷 French, 🇩🇪 German, 🇨🇳 Chinese, 🇯🇵 Japanese).


**🔍 Tech Stack**:

Frontend: Streamlit, HTML/CSS

AI Models: Gemini Pro, OpenAI GPT-3.5 Turbo

Image Generation: Stable Diffusion (diffusers library)

File Handling: pandas, openpyxl, io, json, csv, gspread

Backend: Langchain

**Deployment: Hugging Face ** 
[🚀 Live Demo on Hugging Face](https://huggingface.co/spaces/Dineshmanimela/Ai_For_Marketing)



**Team 🧑‍💻**:

This project was developed during the Workcohol AI Internship by a dedicated team of four members, under the guidance and leadership of Dinesh Kumar Manimela.

**👥 Team Members & Contributions**:


1. Dinesh Kumar Manimela (Team Lead)

i. Lead development and coordination

ii. Designed and integrated advanced features like image & voice input support, and API key management, and content overview image generation, and adding features for getting customized outputs

iii. Improved the overall UI/UX and led final code review

iv. Added key elements such as image in the overview

v. Handled deployment setup and wrote & tested 20+ test cases.

vi. Finalized the project report by redesigning the entire template, thoroughly reviewing, and completing all documentation after minimal initial input from teammates.



2. Chandrika (Team member)

i. Contributed to initial coding and feature implementation

ii. Worked on deployment setup and helped with writing initial test cases

iii. Played a key role in early-stage development and actively participated in codebase improvements


3. Bharath (Team member)

i. Involved in initial coding and report formatting (template) 

iii. Assisted in deployment testing and test case writing

v. partial deployment of first version of your project in hugging face.



4. Srilekha (Team member)

i. Responsible for initial documentation of the project

ii. helped with writing initial test cases 

iii. Contributed to the early structure and content of the project report



## Setup Instructions 🔧

```bash
# Clone the repository
git clone https://github.com/yourusername/ai-marketing-generator.git

# Navigate into the project folder
cd ai-marketing-generator

# Install dependencies
pip install -r requirements.txt

# Run the Streamlit app
streamlit run code.py
