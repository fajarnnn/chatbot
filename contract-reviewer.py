import streamlit as st
import requests
import openai
import base64

# --- Fungsi untuk Mengirim Pesan ke Telegram ---
def send_telegram_message(telegram_token, chat_id, message_text):
    if not telegram_token or not chat_id:
        st.error("Telegram Access Token atau Chat ID belum diatur di sidebar.")
        return False

    url = f"https://api.telegram.org/bot{telegram_token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message_text
    }
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()  # Angkat HTTPError untuk status kode yang buruk (4xx atau 5xx)
        return True
    except requests.exceptions.RequestException as e:
        st.error(f"Gagal mengirim pesan ke Telegram: {e}")
        return False

# --- Fungsi untuk Mengirim File PDF ke Telegram (Placeholder) ---
def send_telegram_pdf(telegram_token, chat_id, pdf_file):
    if not telegram_token or not chat_id:
        st.error("Telegram Access Token atau Chat ID belum diatur di sidebar.")
        return False
    
    # Ini adalah contoh placeholder. Anda perlu mengadaptasi ini untuk mengunggah file PDF yang sebenarnya.
    # Biasanya, Anda akan menggunakan sendDocument atau sendFile.
    # Untuk demonya, saya akan mengirimkan notifikasi teks.
    st.warning("Fungsi pengiriman PDF ke Telegram sedang dikembangkan. Untuk sementara, kami akan mengirimkan notifikasi teks.")
    
    pdf_name = pdf_file.name if pdf_file else "unknown_pdf"
    message_text = f"File PDF '{pdf_name}' telah diterima dan akan diproses. (Fitur pengiriman PDF belum aktif)"
    return send_telegram_message(telegram_token, chat_id, message_text)


# --- Fungsi untuk Berinteraksi dengan OpenAI (Placeholder) ---
def get_openai_response(openai_api_key, prompt):
    if not openai_api_key:
        st.error("OpenAI Access Token belum diatur di sidebar.")
        return "Silakan masukkan OpenAI Access Token Anda."

    openai.api_key = openai_api_key
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",  # Anda bisa mengganti dengan model lain yang relevan
            prompt=prompt,
            max_tokens=150
        )
        return response.choices[0].text.strip()
    except openai.error.OpenAIError as e:
        st.error(f"Gagal berkomunikasi dengan OpenAI: {e}")
        return "Terjadi kesalahan saat mencoba mendapatkan respons dari OpenAI."


# --- Streamlit App ---
st.set_page_config(page_title="Chatbot Telegram & OpenAI")

st.title("🤖 Chatbot Integrasi Telegram & OpenAI")

st.write("""
Halo! Selamat datang di Chatbot Integrasi Telegram & OpenAI.
**Saat ini, chatbot ini dirancang untuk mengirimkan file PDF Anda ke Telegram.**
""")
st.info("Silakan unggah file PDF Anda di bawah, atau kirim pesan teks untuk berinteraksi dengan OpenAI.")

# --- Sidebar untuk Konfigurasi ---
st.sidebar.header("Konfigurasi API")
telegram_access_token = st.sidebar.text_input("Telegram Bot Access Token", type="password")
telegram_chat_id = st.sidebar.text_input("Telegram Chat ID", help="Dapatkan dari @userinfobot di Telegram")
openai_access_token = st.sidebar.text_input("OpenAI API Key", type="password")

st.sidebar.markdown("---")
st.sidebar.write("Pastikan token dan ID Anda sudah benar.")

# --- Input untuk File PDF ---
st.header("Unggah File PDF Anda")
uploaded_file = st.file_uploader("Pilih file PDF", type="pdf")

if uploaded_file is not None:
    st.write(f"File PDF terpilih: **{uploaded_file.name}**")
    if st.button("Kirim PDF ke Telegram"):
        if send_telegram_pdf(telegram_access_token, telegram_chat_id, uploaded_file):
            st.success(f"File PDF '{uploaded_file.name}' berhasil dikirim (notifikasi) ke Telegram!")
        else:
            st.error("Gagal mengirimkan file PDF ke Telegram.")

st.markdown("---")

# --- Input untuk Chatbot Teks (OpenAI) ---
st.header("Chat dengan OpenAI")
user_input = st.text_input("Tulis pesan Anda di sini:")

if st.button("Kirim Pesan"):
    if user_input:
        with st.spinner("Mendapatkan respons dari OpenAI..."):
            openai_response = get_openai_response(openai_access_token, user_input)
            st.write(f"**Anda:** {user_input}")
            st.write(f"**Chatbot (OpenAI):** {openai_response}")

        # Opsi: Kirim pesan chatbot ke Telegram juga
        if st.checkbox("Kirim pesan ini ke Telegram juga?"):
            message_to_telegram = f"Pesan dari Chatbot: {user_input}\nRespons OpenAI: {openai_response}"
            if send_telegram_message(telegram_access_token, telegram_chat_id, message_to_telegram):
                st.success("Pesan berhasil dikirim ke Telegram!")
            else:
                st.error("Gagal mengirim pesan ke Telegram.")
    else:
        st.warning("Silakan masukkan pesan untuk berinteraksi dengan OpenAI.")

st.markdown("---")
st.write("Dibuat dengan ❤️ menggunakan Streamlit.")
