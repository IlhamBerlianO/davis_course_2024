import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
from gtts import gTTS
from deep_translator import GoogleTranslator
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

# Inisialisasi objek Translator
translator = GoogleTranslator(source='en', target='id')

# Fungsi untuk merubah teks deskripsi menjadi suara
def text_to_speech(text):
    tts = gTTS(text=text, lang='en')  # Menggunakan gTTS untuk mengonversi teks ke suara dalam bahasa Inggris
    speech = io.BytesIO()
    tts.write_to_fp(speech)
    return speech.getvalue()

# Tambahkan tombol untuk membaca deskripsi perusahaan
if st.button("Translate ke Indonesia"):
    # Translate deskripsi dari bahasa Inggris ke bahasa Indonesia
    description_id = translator.translate(descriptions[index])
    descriptions[index] = description_id

# Tambahkan tombol untuk membaca deskripsi perusahaan
if st.button("Baca Deskripsi"):
    speech_bytes = text_to_speech(descriptions[index])
    st.audio(speech_bytes, format='audio/mp3')

st.write(descriptions[index])


st.write(f'Created by Ilham Berlian Oktavio')
