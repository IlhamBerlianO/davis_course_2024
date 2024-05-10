import streamlit as st
import matplotlib.pyplot as plt
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

# # Plot grafik
plt.figure(figsize=(10, 6))
plt.barh(companies, prices, color='#398bff')
plt.xlabel('Harga Saham ($)')
plt.ylabel('Perusahaan')
plt.title('Grafik Saham Perusahaan 2024')
plt.gca().invert_yaxis() 
st.pyplot(plt)

# Judul aplikasi
st.title('Profil Perusahaan')

# Pilih saham dari dropdown
selected_stock = st.selectbox('Pilih Perusahaan:', companies)

# Temukan indeks saham yang dipilih di daftar perusahaan
index = companies.index(selected_stock)

# Tampilkan detail perusahaan yang dipilih
st.write(f'Nama Perusahaan: {companies[index]}')
st.write(f'Harga Saham: ${prices[index]}')
st.write(f'Deskripsi Perusahaan:')
st.write(descriptions[index])

# Tambahkan tombol untuk membaca deskripsi perusahaan
if st.button("Translate ke Indonesia"):
    def translate_text(text):
        try:
            translator = Translator()
            translated_text = translator.translate(text, src='en', dest='id')
            return translated_text.text
        except Exception as e:
            st.error(f"Error: {e}")
            return None
    
    translated_text = translate_text(descriptions[index])
    if translated_text:
        st.write("Terjemahan ke Bahasa Indonesia:")
        st.write(translated_text)

# Fungsi untuk merubah teks deskripsi menjadi suara
def text_to_speech(text):
    tts = gTTS(text=text, lang='en')  # Menggunakan gTTS untuk mengonversi teks ke suara dalam bahasa Inggris
    speech = io.BytesIO()
    tts.write_to_fp(speech)
    return speech.getvalue()

# Tambahkan tombol untuk membaca deskripsi perusahaan
if st.button("Baca Deskripsi"):
    speech_bytes = text_to_speech(descriptions[index])
    st.audio(speech_bytes, format='audio/mp3')



st.write(f'Created by Ilham Berlian Oktavio')
