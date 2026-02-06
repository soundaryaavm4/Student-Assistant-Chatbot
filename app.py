import streamlit as st
from datetime import datetime
import uuid
import json
import os
from groq import Groq
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from PIL import Image
import pytesseract

# ---------------- ENV + GROQ ----------------

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def chat_completion(messages, model="llama-3.1-8b-instant"):
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0.3,
    )
    return response.choices[0].message.content


# ---------------- TEXT EXTRACTION ----------------

def extract_text_from_file(uploaded_file):
    file_type = uploaded_file.type

    if file_type == "application/pdf":
        reader = PdfReader(uploaded_file)
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""
        return text

    elif file_type.startswith("image"):
        image = Image.open(uploaded_file)
        return pytesseract.image_to_string(image)

    elif file_type == "text/plain":
        return uploaded_file.read().decode("utf-8")

    return ""


# ---------------- STREAMLIT CHAT ----------------

DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)

def load_conversations():
    if "conversations" not in st.session_state:
        st.session_state.conversations = {}
        st.session_state.active_conversation_id = None

def create_new_conversation():
    cid = str(uuid.uuid4())
    st.session_state.conversations[cid] = {
        "id": cid,
        "title": "New chat",
        "created_at": datetime.now().isoformat(),
        "messages": [],
    }
    st.session_state.active_conversation_id = cid

def get_active_conversation():
    cid = st.session_state.active_conversation_id
    if not cid:
        create_new_conversation()
        cid = st.session_state.active_conversation_id
    return st.session_state.conversations[cid]

def save_conversation(conv):
    with open(os.path.join(DATA_DIR, f"{conv['id']}.json"), "w") as f:
        json.dump(conv, f, indent=2)


def main():
    st.set_page_config(page_title="Student Assistant", layout="wide")
    load_conversations()

    st.title("📚 Student Assistant Chatbot")

    with st.sidebar:
        if st.button("➕ New chat", use_container_width=True):
            create_new_conversation()

        for cid, conv in st.session_state.conversations.items():
            if st.button(conv["title"], key=cid):
                st.session_state.active_conversation_id = cid

    conv = get_active_conversation()

    for msg in conv["messages"]:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # -------- SMALL UPLOAD ICON ONLY --------

    uploaded_files = st.file_uploader(
        "",
        type=["pdf", "png", "jpg", "jpeg", "txt"],
        accept_multiple_files=True,
        label_visibility="collapsed"
    )

    st.markdown("""
    <style>
    [data-testid="stFileUploader"] div[data-testid="stFileUploaderDropzone"]{
        display:none;
    }

    [data-testid="stFileUploader"] button {
        position: fixed;
        bottom: 26px;
        right: 90px;
        width: 36px;
        height: 36px;
        border-radius: 50%;
        font-size: 18px;
    }
    </style>
    """, unsafe_allow_html=True)

    # ---------------------------------------

    notes_text = ""
    if uploaded_files:
        parts = []
        for f in uploaded_files:
            parts.append(extract_text_from_file(f))
        notes_text = "\n\n".join(parts)

    user_prompt = st.chat_input("Ask your study question...")

    if user_prompt:
        conv["messages"].append({"role": "user", "content": user_prompt})

        system_prompt = "You are a STUDENT STUDY ASSISTANT. Give concise structured answers."

        messages = [{"role": "system", "content": system_prompt}]

        if notes_text:
            messages.append({"role": "system", "content": notes_text[:12000]})

        for m in conv["messages"]:
            messages.append({"role": m["role"], "content": m["content"]})

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                answer = chat_completion(messages)
                st.markdown(answer)

        conv["messages"].append({"role": "assistant", "content": answer})

        if conv["title"] == "New chat":
            conv["title"] = user_prompt[:30]

        save_conversation(conv)


if __name__ == "__main__":
    main()
