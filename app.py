import streamlit as st
import os
from dotenv import load_dotenv
from groq import Groq

# -------------------------------------------------------
# STREAMLIT CONFIG
# -------------------------------------------------------
st.set_page_config(
    page_title="Belajar Akuntansi",
    layout="centered"
)

# -------------------------------------------------------
# LOAD ENV
# -------------------------------------------------------
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    st.error("❌ API Key Groq tidak ditemukan.")
    st.stop()

client = Groq(api_key=GROQ_API_KEY)

# -------------------------------------------------------
# CUSTOM CSS (WhatsApp style rolling chat)
# -------------------------------------------------------
st.markdown("""
<style>

body {
    background-color: #f5f7fa;
    font-family: 'Roboto', sans-serif;
}

/* Container utama */
.chat-box {
    max-width: 650px;
    margin: auto;
    background: #ffffff;
    padding: 15px;
    border-radius: 10px;
}

/* Bubble User */
.chat-bubble-user {
    background: #d1e7ff;
    padding: 10px 14px;
    border-radius: 15px;
    margin: 8px 0;
    max-width: 75%;
    margin-left: auto;
    color: black;
    animation: fadeIn 0.25s ease-in;
}

/* Bubble Bot */
.chat-bubble-bot {
    background: #ffffff;
    padding: 10px 14px;
    border-radius: 15px;
    border: 1px solid #ddd;
    margin: 8px 0;
    max-width: 75%;
    margin-right: auto;
    color: black;
    animation: fadeIn 0.25s ease-in;
}

/* Header */
.header {
    text-align: center;
    padding: 15px;
    background: #0dbf6f;
    color: white;
    border-radius: 0 0 10px 10px;
    font-size: 24px;
    font-weight: bold;
    margin-bottom: 20px;
}

/* Animasi bubble */
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(5px); }
    to { opacity: 1; transform: translateY(0); }
}

</style>
""", unsafe_allow_html=True)

# -------------------------------------------------------
# HEADER
# -------------------------------------------------------
st.markdown('<div class="header">Selamat Datang di ChatBot Belajar Akuntansi</div>', unsafe_allow_html=True)

# -------------------------------------------------------
# SESSION STATE
# -------------------------------------------------------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# -------------------------------------------------------
# TAMPILAN CHAT (rolling)
# -------------------------------------------------------
st.markdown('<div class="chat-box">', unsafe_allow_html=True)

for role, text in st.session_state.chat_history:
    if role == "user":
        st.markdown(f'<div class="chat-bubble-user">{text}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="chat-bubble-bot">{text}</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# -------------------------------------------------------
# INPUT PENGGUNA (seperti WA)
# -------------------------------------------------------
user_input = st.text_input(
    "Ketik pertanyaan atau minta latihan soal...",
    placeholder="contoh: jelaskan persamaan dasar akuntansi"
)

# -------------------------------------------------------
# PROSES JAWABAN
# -------------------------------------------------------
if user_input:

    # Simpan pesan user
    st.session_state.chat_history.append(("user", user_input))

    system_prompt = """
    Kamu adalah asisten belajar akuntansi yang santai, jelas, dan mudah dipahami.
    Gunakan bahasa chill namun tetap rapi.
    
    Mode:
    - Jika user bertanya konsep → jelaskan langkah demi langkah.
    - Jika user minta latihan soal → berikan 1–3 soal + jawabannya setelah user mencoba.
    - Jangan mengulang salam atau menyimpulkan percakapan lama.
    """

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_input}
        ],
        temperature=0.2
    )

    bot_reply = response.choices[0].message.content

    # Tambahkan jawaban bot
    st.session_state.chat_history.append(("assistant", bot_reply))

    st.rerun()
