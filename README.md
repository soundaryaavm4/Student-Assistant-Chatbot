# 📚 Student Assistant Chatbot (Streamlit + Groq)

A simple Streamlit-based Student Assistant chatbot that supports:

✅ Groq LLM (llama-3.1-8b-instant)  
✅ Chat interface  
✅ Upload PDF / Image / TXT notes  
✅ OCR from images  
✅ Conversation history  
✅ Sidebar chat sessions  
✅ Floating upload button  
✅ No drag & drop UI  

---

## 🚀 Features

- Ask study-related questions
- Upload notes (PDF / Images / TXT)
- OCR support using Tesseract
- Groq-powered responses
- Chat history stored locally
- Multiple conversations
- Clean UI with small upload icon

---

## 📁 Project Structure

chat/
│
├── app.py
├── req.txt
├── .env
└── data/


---

## 🔑 Environment Setup

Create `.env` file:

GROQ_API_KEY=your_api_key_here


---

## 📦 Install Dependencies

    ```bash
    pip install -r req.txt
    macOS OCR requirement:
    brew install tesseract

▶️ Run Application
      
      streamlit run app.py
      Browser will open automatically.

🧠 Model Used
    
    llama-3.1-8b-instant

📌 Notes

    Uploaded files are processed locally

    Conversations saved inside data/

    Images use Tesseract OCR

    PDFs extracted using PyPDF2

✨ Future Improvements

    Streaming responses

    Export chats

    UI themes

    User authentication

    Deployment

