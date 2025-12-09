import streamlit as st
import os
from dotenv import load_dotenv
from groq import Groq

# ============= CONFIG =============
st.set_page_config(page_title="Belajar Akuntansi", layout="centered")

# Load environment variable

api_key = os.getenv("GROQ_API_KEY")

# ============= CSS =============
st.markdown("""
<style>
body {
    background-color: #f2f4f7;
    font-family: 'Inter', sans-serif;
}
.header-box {
    text-align: center;
    padding: 18px;
    background: #7b4bc2;
    color: white;
    font-size: 24px;
    border-radius: 0 0 12px 12px;
    font-weight: 600;
    margin-bottom: 10px;
}
.chat-container {
    width: 100%;
    max-width: 650px;
    margin: auto;
    padding: 5px 15px;
}
.bot-bubble, .user-bubble {
    padding: 12px 16px;
    border-radius: 16px;
    margin: 8px 0;
    max-width: 80%;
    font-size: 16px;
}
.bot-bubble {
    background: #ffffff;
    border: 1px solid #e5e5e5;
    color: #000;
    margin-right: auto;
}
.user-bubble {
    background: #cfe1ff;
    color: #000;
    margin-left: auto;
}
</style>
""", unsafe_allow_html=True)

# ============= HEADER =============
st.markdown('<div class="header-box">Belajar Akuntansi</div>', unsafe_allow_html=True)

# ============= SESSION FIX =============
if "history" not in st.session_state:
    st.session_state.history = [
        ("assistant", "Halo! Selamat datang di ChatBot **Belajar Akuntansi**. Mau mulai dari penjelasan materi atau latihan soal?")
    ]

# ============= TAMPILKAN CHAT =============
st.markdown('<div class="chat-container">', unsafe_allow_html=True)

for role, text in st.session_state.history:
    if role == "assistant":
        st.markdown(f'<div class="bot-bubble">{text}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="user-bubble">{text}</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# ============= INPUT FIX =============
user_input = st.text_input(
    "Ketik pertanyaanmu…",
    placeholder="Tulis sesuatu...",
    key="text_input"
)

# Jika ada input baru
if user_input and user_input.strip():
    message = user_input.strip()
    st.session_state.history.append(("user", message))

    # Masukkan pesan user satu kali
    st.session_state.history.append(("user", message))

    # Panggil LLM tanpa menduplikasi history
    try:
        messages = [{"role": "system", "content": "Kamu adalah chatbot akuntansi yang chill, ramah, dan mudah dipahami."}]
        messages += [{"role": role, "content": content} for role, content in st.session_state.history]

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages
        )
        bot_reply = response.choices[0].message["content"]
    except Exception as e:
        bot_reply = f"❌ Terjadi error saat memanggil API: {e}"

    st.session_state.history.append(("assistant", bot_reply))

    # Reset input tanpa error
    st.session_state.text_input = ""

    # Refresh tampilan
    st.rerun()











