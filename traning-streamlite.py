import streamlit as st
import openai
import PyPDF2
import io
import os
from dotenv import load_dotenv

# Muat variabel lingkungan dari file .env
load_dotenv()

def extract_text_from_pdf(pdf_file):
    """Mengekstrak teks dari file PDF yang diunggah."""
    reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page_num in range(len(reader.pages)):
        text += reader.pages[page_num].extract_text()
    return text

def analyze_contract_with_openai(contract_text, openai_api_key):
    """Mengirim teks kontrak ke OpenAI untuk analisis."""
    openai.api_key = openai_api_key
    try:
        response = openai.chat.completions.create(
            model="gpt-4",  # Anda bisa mencoba "gpt-3.5-turbo" untuk opsi yang lebih cepat
            messages=[
                {"role": "system", "content": "Anda adalah asisten AI yang ahli dalam menganalisis dokumen kontrak. Berikan ringkasan poin-poin penting, klausul-klausul utama, potensi risiko, dan rekomendasi terkait kontrak yang diberikan."},
                {"role": "user", "content": f"Tolong analisis kontrak berikut ini:\n\n{contract_text}"}
            ],
            max_tokens=1500,
            temperature=0.7,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Terjadi kesalahan saat memanggil API OpenAI: {e}"

st.set_page_config(layout="wide", page_title="Analisis Kontrak PDF")

st.title("📄 Aplikasi Analisis Kontrak PDF dengan OpenAI")
st.markdown("""
Aplikasi ini memungkinkan Anda mengunggah dokumen kontrak dalam format PDF dan mendapatkan analisis mendalam menggunakan model AI dari OpenAI.
""")

# Sidebar untuk API Key
with st.sidebar:
    st.header("Konfigurasi API")
    openai_api_key = st.text_input(
        "Masukkan OpenAI API Key Anda",
        type="password",
        value=os.getenv("OPENAI_API_KEY") # Mengambil dari .env jika ada
    )
    st.markdown("Dapatkan API Key Anda dari [OpenAI Platform](https://platform.openai.com/account/api-keys)")

# Main content
st.header("Unggah Dokumen Kontrak Anda (PDF)")
uploaded_file = st.file_uploader("Pilih file PDF", type=["pdf"])

analysis_result = None

if uploaded_file is not None:
    st.subheader("Pratinjau Dokumen")
    # Tampilkan nama file yang diunggah
    st.write(f"Nama file: {uploaded_file.name}")

    # Ekstrak teks
    with st.spinner("Mengekstrak teks dari PDF..."):
        contract_text = extract_text_from_pdf(uploaded_file)
    
    # Tampilkan sebagian teks yang diekstrak (opsional)
    # st.subheader("Teks yang Diekstrak (Sebagian)")
    # st.text_area("Konten PDF:", contract_text[:1000] + "..." if len(contract_text) > 1000 else contract_text, height=200, disabled=True)

    if not openai_api_key:
        st.warning("Mohon masukkan OpenAI API Key Anda di sidebar untuk melanjutkan.")
    else:
        if st.button("Mulai Analisis Kontrak"):
            if contract_text:
                with st.spinner("Menganalisis kontrak dengan OpenAI... Ini mungkin memerlukan beberapa menit."):
                    analysis_result = analyze_contract_with_openai(contract_text, openai_api_key)
                st.success("Analisis selesai!")
            else:
                st.error("Gagal mengekstrak teks dari PDF. Pastikan file tidak kosong atau rusak.")

if analysis_result:
    st.subheader("Hasil Analisis Kontrak")
    st.markdown(analysis_result)

st.markdown("---")
st.caption("Dibuat dengan ❤️ oleh Asisten AI")
