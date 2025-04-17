## 📄 Full Report  
You can download the full documentation [here](https://github.com/dineshkumar8464/AI-for-Marketing-Project/blob/master/AI_FOR_MARKETING_REPORT.pdf).


# 🧠 AI Marketing Generator | Streamlit App 🚀  
_A project developed during my AI Internship at Workcohol_

## Developed by: Dinesh Kumar Manimela along with the Team  
📧 dineshmanimela088@gmail.com  
🌐 www.workcohol.com  
Chandrika, Bharath Sekhar, Sri lekha

---

## 📌 Project Overview

**AI Marketing Generator** is a web-based application that leverages **Gemini (Google)** and **GPT-3.5 (OpenAI)** via **LangChain** to automate the creation of:
- Marketing slogans
- Ad copies
- Campaign ideas

It supports **bulk content generation**, **custom tones**, **SEO optimization**, **Image genration** from selected overview and **advanced export features**. The app also accepts **voice and image inputs**, this was partially implemented for accessibility.

---

## 🎯 Objective

To streamline and scale marketing content creation using LLMs, enabling businesses and individuals to:
- Save time
- Reduce costs
- Maintain branding consistency
- Automate repetitive content generation tasks

---


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





## DINESH KUMAR MANIMELA:  My Individual Contributions

As an AI Engineer Intern and contributor to this project with the team lead, I was responsible for:

- ✅ **Multi-model Integration**: Integrated Gemini and GPT-3.5 using LangChain for seamless switching and comparison.
- ✅ **Parallel Bulk Generation**: Implemented `ThreadPoolExecutor` for faster processing of bulk CSV data.
- ✅ **Google Sheets Export**: Added real-time export functionality using `gspread` for cloud-based content storage.
- ✅ **Session Management**: Preserved outputs using `st.session_state` to allow model switching without data loss.
- ✅ **Error Handling**: Built robust mechanisms for failed API responses, missing data, and malformed files.
- ✅ **Image generation from text-to-image**: Built robust mechanisms for failed API responses, missing data, and malformed files.
- ✅ **Partial Voice/Image Input Support**: Used `SpeechRecognition` for voice-to-text and `pytesseract` for OCR on images.

---

## 🛠️ Technology Stack

Frontend: Streamlit, CSS for minner Ui tweaks

AI Models: Gemini Pro, OpenAI GPT-3.5 Turbo

Image Generation: Stable Diffusion (diffusers library)

File Handling: pandas, openpyxl, io, json, csv, gspread

Backend: Langchain

---

## 🔄 Workflow

1. User inputs product name(s), tone, word limit, and platform.
2. Select AI model: **GPT-3.5** or **Gemini**.
3. AI generates content → user reviews → visual content can be generated.
4. Export content via:
   - 📄 CSV, Excel, JSON, Text
   - ☁️ Google Sheets (real-time cloud export)

---

## 🧪 Test Cases

- ✅ Valid/Invalid CSV Upload
- ✅ Valid/Invalid Product Input names
- ✅ Empty Row Handling
- ✅ API Failure Simulation
- ✅ Language & Tone Selection
- ✅ Export Function Verification
- ✅ Large File Stress Testing

---

## 📦 Deployment

The application is deployed on **Hugging Face Spaces**:  
[🚀 Live Demo on Hugging Face](https://huggingface.co/spaces/Dineshmanimela/Ai_For_Marketing)
 

---

## 📈 Future Enhancements

- Claude and Mistral API integration
- Full voice/image input UI
- Social media-specific content adaptation
- Engagement score prediction

---

## 📚 References

- [LangChain Docs](https://python.langchain.com/docs/)
- [OpenAI API](https://platform.openai.com/docs/)
- [Gemini API (Google)](https://ai.google.dev/)
- [gspread for Google Sheets](https://gspread.readthedocs.io/)
- [SpeechRecognition](https://pypi.org/project/SpeechRecognition/)
- [Tesseract OCR](https://tesseract-ocr.github.io/)

---

## 🙌 Acknowledgements

Thanks to **Workcohol** for providing a learning-focused internship environment and support throughout the development process.

---

> *“AI isn’t replacing marketers—it’s empowering them.”*



**Team 🧑‍💻**:

This project was developed during the Workcohol AI Internship by a dedicated team of four members, under the guidance and leadership of Dinesh Kumar Manimela.


**👥 Team Members & Contributions**:

1. Dinesh Kumar Manimela (Team Lead): 

2. Chandrika (Team member)

 - i. Contributed to initial coding and feature implementation

 - ii. Worked on deployment setup and helped with writing initial test cases

 - iii. Played a key role in early-stage development and actively participated in codebase improvements



3. Bharath (Team member)

- i. Involved in initial coding and report formatting (template) 

- iii. Assisted in deployment testing and test case writing

- v. partial deployment of first version of your project in hugging face.



4. Srilekha (Team member)

- i. Responsible for initial documentation of the project

- ii. helped with writing initial test cases 

- iii. Contributed to the early structure and content of the project report





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
