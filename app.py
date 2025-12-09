import streamlit as st
import os
from dotenv import load_dotenv
from groq import Groq

# ============= CONFIG =============
st.set_page_config(page_title="Belajar Akuntansi", layout="centered")

load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    st.error("❌ API Key Groq tidak ditemukan. Pastikan sudah di-set di .env atau di Streamlit Secrets.")
    st.stop()

client = Groq(api_key=api_key)
# ============= CSS =============
st.markdown("""
<style>
body { background-color: #f2f4f7; font-family: 'Inter', sans-serif; }
.header-box { text-align: center; padding: 18px; background: #7b4bc2; color: white; font-size: 24px; border-radius: 0 0 12px 12px; font-weight: 600; margin-bottom: 10px; }
.chat-container { width: 100%; max-width: 650px; margin: auto; padding: 5px 15px; }
.bot-bubble, .user-bubble { padding: 12px 16px; border-radius: 16px; margin: 8px 0; max-width: 80%; font-size: 16px; }
.bot-bubble { background: #ffffff; border: 1px solid #e5e5e5; color: #000; margin-right: auto; }
.user-bubble { background: #cfe1ff; color: #000; margin-left: auto; }
</style>
""", unsafe_allow_html=True)

# ============= HEADER =============
st.markdown('<div class="header-box">Belajar Akuntansi</div>', unsafe_allow_html=True)

# ============= SESSION STATE =================
if "history" not in st.session_state:
    st.session_state.history = [
        ("assistant", "Halo! Selamat datang di ChatBot **Belajar Akuntansi**. Mau mulai dari penjelasan materi atau latihan soal?")
    ]

# ============= TAMPILKAN CHAT =================
st.markdown('<div class="chat-container">', unsafe_allow_html=True)
for role, text in st.session_state.history:
    if role == "assistant":
        st.markdown(f'<div class="bot-bubble">{text}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="user-bubble">{text}</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)
# ================= INPUT USER =================
with st.form("chat_form", clear_on_submit=True):
    user_input = st.text_input("Ketik pertanyaanmu…", placeholder="Tulis sesuatu...")
    submitted = st.form_submit_button("Kirim")
    if submitted and user_input.strip():
        st.session_state.history.append(("user", user_input.strip()))
        # Panggil API seperti biasa



