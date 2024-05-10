import streamlit as st
import pandas as pd
from gtts import gTTS
from googletrans import Translator
import io
import base64

# Judul aplikasi
st.title('Saham 2024')

# Deskripsi
st.write(f'Visualisasi data saham dengan menggunakan data dari www.investing.com')

# Membaca file excel
baca = pd.read_excel("Saham 2024.xlsx")

# Ambil data perusahaan dan harga dari hasil
companies = baca['Company'].tolist()
prices = baca['Price'].tolist()
descriptions = baca['Description'].tolist()

# Plot grafik
st.bar_chart(baca.set_index('Company')['Price'])

# Judul aplikasi
st.title('Company Profile')

# Pilih saham dari dropdown
selected_stock = st.selectbox('Choose Company:', companies)

# Pilih bahasa untuk deskripsi
selected_lang = st.selectbox('Choose Language:', ['English', 'Indonesian'])

# Temukan indeks saham yang dipilih di daftar perusahaan
index = companies.index(selected_stock)

# Tampilkan detail perusahaan yang dipilih dalam bahasa Inggris atau bahasa Indonesia
st.write(f'Company name: {companies[index]}')
st.write(f'Stock Price: ${prices[index]}')
st.write(f'Company Description ({selected_lang}):')
if selected_lang == 'English':
    st.write(descriptions[index])
else:
    # Terjemahkan deskripsi ke bahasa Indonesia
    translator = Translator()
    translated_description = translator.translate(descriptions[index], src='en', dest='id').text
    st.write(translated_description)

# Fungsi untuk mengonversi teks menjadi suara
def text_to_speech(text, lang='id'):
    tts = gTTS(text=text, lang=lang)
    speech = io.BytesIO()
    tts.write_to_fp(speech)
    return speech.getvalue()

# Tambahkan tombol untuk membaca deskripsi perusahaan
if st.button("Baca Deskripsi"):
    lang_code = 'en' if selected_lang == 'English' else 'id'
    speech_bytes = text_to_speech(descriptions[index], lang=lang_code)
    st.audio(speech_bytes, format='audio/mp3')

# Tambahkan tombol untuk mengubah bahasa deskripsi perusahaan
if selected_lang == 'English':
    if st.button("Translate to Indonesian"):
        translated_description = translator.translate(descriptions[index], src='en', dest='id').text
        st.write(translated_description)

st.write(f'Created by Ilham Berlian Oktavio')
