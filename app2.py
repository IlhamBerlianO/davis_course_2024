import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import openpyxl
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

# Fungsi untuk merubah bahasa untuk deskripsi perusahaan
def text_to_speech(text):
    tts = gTTS(text=text, lang='en')
    speech = io.BytesIO()
    tts.write_to_fp(speech)
    return speech.getvalue()

# Tambahkan tombol untuk merubah bahasa untuk deskripsi perusahaan
if st.button("Translate ke Indonesia"):
    # Translate deskripsi dari bahasa Inggris ke bahasa Indonesia
    descriptions_id = [translator.translate(desc, src='en', dest='id').text for desc in descriptions_en]
    # # Tampilkan deskripsi perusahaan yang telah diterjemahkan
    # st.write(f'Company Description (Indonesian):')
    # st.write(descriptions_id[index])
    # Perbarui deskripsi yang ditampilkan
    descriptions_en[index] = descriptions_id[index]

# Tambahkan tombol untuk membaca deskripsi perusahaan
if st.button("Baca Deskripsi"):
    # Jika deskripsi dalam bahasa Inggris
    if "descriptions_id" not in locals():
        speech_bytes = text_to_speech(descriptions_en[index])
    # Jika deskripsi telah diterjemahkan ke bahasa Indonesia
    else:
        speech_bytes = text_to_speech(descriptions_id[index], lang='id')
    st.audio(speech_bytes, format='audio/mp3')

st.write(f'Created by Ilham Berlian Oktavio')
