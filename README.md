# AI Marketing Generator | Streamlit App  
Welcome to the repository for the project on the Development of an Platform called AI Powered Marketing Generator using langchain.
_A project developed during my AI Internship at Workcohol_

---

## Project Overview

**AI Marketing Generator** is a web-based application that leverages **Gemini (Google)** and **GPT-3.5 (OpenAI)** via **LangChain** to automate the creation of:
- Marketing slogans
- Ad copies
- Campaign ideas

It supports **bulk content generation**, **custom tones**, **SEO optimization**, **Image genration** from selected overview and **advanced export features**. The app also accepts **voice and image inputs**, this was partially implemented for accessibility.

---

## Objective

To streamline and scale marketing content creation using LLMs, enabling businesses and individuals to:
- Save time
- Reduce costs
- Maintain branding consistency
- Automate repetitive content generation tasks

---


## Features:

1. Single Content Generation: Instantly generate engaging marketing content using either Gemini Pro or OpenAI models.
2. Bulk Content Generation: Upload an Excel file and generate content for multiple entries of 20 productsms at once.
3. Export Options: Download your content as .csv, .json, .txt, or even export directly to Google Sheets.
4. Image Generation: Powered by Stable Diffusion, convert selected content into stunning visuals.
5. Image-to-Text Input (Coming Soon): Upload an image and extract text to generate content from it.
6. Voice-to-Text Input (Coming Soon): Speak your ideas and let the app generate marketing content from your voice input.
7. User Interface (UI): Designed with Stream lit, providing an intuitive and user-friendly experience.
8. AI Model Integration (Gemini & GPT-3.5):	Incorporates Google Gemini Pro (gemini-2.5-pro-exp-03-25) and OpenAI’s GPT-3.5 Turbo for content generation. Users can switch btw models to compare outputs.
9. Content Customization: Users can adjust tone, choose platform, set word limit & SEO, and select language
10. Brand and Product Input Handling: This makes the AI more flexible and context-aware in content generation.

---


## Workflow

1. User inputs product name(s), tone, word limit, and platform.
2. Select AI model: **GPT-3.5** or **Gemini**.
3. AI generates content → user reviews → visual content can be generated.
4. Export content via:
   - CSV, Excel, JSON, Text
   - Google Sheets (real-time cloud export)

---

## Deployment:

www.workcohol.com  
Dinesh- Team Lead, Chandrika, Bharath Sekhar, Sri lekha

The application is deployed on **Hugging Face Spaces**:  
[Live Demo on Hugging Face](https://huggingface.co/spaces/Dineshmanimela/Ai_For_Marketing)
 
[Watch Demo Video on LinkedIn](https://www.linkedin.com/posts/dinesh-kumar-manimela-b8992027b_ai-marketing-genai-activity-7318560857062350848-0qQT)

---

## References and acknowledgements

- [LangChain Docs](https://python.langchain.com/docs/)
- [OpenAI API](https://platform.openai.com/docs/)
- [Gemini API (Google)](https://ai.google.dev/)
- [gspread for Google Sheets](https://gspread.readthedocs.io/)
- [SpeechRecognition](https://pypi.org/project/SpeechRecognition/)
- [Tesseract OCR](https://tesseract-ocr.github.io/)


Thanks to **Workcohol** for providing a learning-focused internship environment and support throughout the development process.

---

> *“AI isn’t replacing marketers—it’s empowering them.”*

---

## Contact:

Feel free to reach out to me at dineshmanimela088@gmail.com for any questions, feedback, or collaboration opportunities.
