import streamlit as st
import xlsxwriter
import matplotlib.pyplot as plt
import pandas as pd
import openpyxl

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
st.title('Company Profile')

# Pilih saham dari dropdown
selected_stock = st.selectbox('Choose Company:', companies)

# Temukan indeks saham yang dipilih di daftar perusahaan
index = companies.index(selected_stock)

# Tampilkan detail perusahaan yang dipilih
st.write(f'Company name: {companies[index]}')
st.write(f'Stock Price: ${prices[index]}')
st.write(f'Company Description:')
st.write(descriptions[index])

st.write(f'Nama : Ilham Berlian Oktavio')
st.write(f'NPM : 21082010034')
