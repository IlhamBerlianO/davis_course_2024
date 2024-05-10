import streamlit as st
import cloudscraper 
import xlsxwriter
import matplotlib.pyplot as plt
import pandas as pd
from scrapy.crawler import CrawlerProcess
from bs4 import BeautifulSoup 

# Daftar URL saham
urls = [
    'https://www.investing.com/equities/nike',
    'https://www.investing.com/equities/coca-cola-co',
    'https://www.investing.com/equities/microsoft-corp',
    'https://www.investing.com/equities/3m-co',
    'https://www.investing.com/equities/american-express',
    'https://www.investing.com/equities/amgen-inc',
    'https://www.investing.com/equities/apple-computer-inc',
    'https://www.investing.com/equities/boeing-co',
    'https://www.investing.com/equities/cisco-sys-inc',
    'https://www.investing.com/equities/goldman-sachs-group',
    'https://www.investing.com/equities/ibm',
    'https://www.investing.com/equities/intel-corp',
    'https://www.investing.com/equities/jp-morgan-chase',
    'https://www.investing.com/equities/mcdonalds',
    'https://www.investing.com/equities/salesforce-com',
    'https://www.investing.com/equities/verizon-communications',
    'https://www.investing.com/equities/visa-inc',
    'https://www.investing.com/equities/wal-mart-stores',
    'https://www.investing.com/equities/disney'
]

# Judul aplikasi
st.title('Saham 2024')

# Deskripsi
st.write(f'Visualisasi data saham dengan menggunakan data dari www.investing.com')

# Buat objek scraper
scraper = cloudscraper.create_scraper(delay=10, browser="chrome")

# List untuk menyimpan hasil(company, price) dari setiap URL
data = []

# Loop melalui setiap URL dan ambil kontennya
for url in urls:
    try:
        # Ambil konten dari URL saat ini
        content = scraper.get(url).text
        # print(f"Sukses mengambil konten dari {url}")
        soup = BeautifulSoup(content, 'html.parser')
        # Mendapatkan data yang di inginkan
        company = soup.find('h1', {'class': 'mb-2.5 text-left text-xl font-bold leading-7 text-[#232526] md:mb-2 md:text-3xl md:leading-8 rtl:soft-ltr'}).text
        price = soup.find('div', {'class': 'text-5xl/9 font-bold text-[#232526] md:text-[42px] md:leading-[60px]'}).text
        # print(f"Nama Company = {company}", f"Saham saat ini = {price}")
        
        # Menemukan link profil perusahaan
        links = soup.find_all('a', {'class':'hover:text-[#1256a0] hover:underline'})
        
        # Loop melalui setiap link yang ditemukan
        for link in links:
            try:
                # Ambil URL dari link
                href = link.get('href')
                # Memeriksa apakah link mengandung kata "company-profile" (Memastikan hanya yang mengandung kata saja yang dipilih)
                if "company-profile" in href:
                    profile_url = "https://www.investing.com" + href
                    content1 = scraper.get(profile_url).text
                    soup1 = BeautifulSoup(content1, 'html.parser')
                    # print(f"Sukses mengambil konten dari {profile_url}")
                    # Mendapatkan data yang di inginkan
                    deskripsi = soup1.find('p', {'id': 'profile-fullStory-showhide'}).text
                    # print(f"Deskripsi Perusahaan: {deskripsi}")
            except Exception as r:
                print(f"Gagal mengambil konten dari {profile_url}: {str(r)}")
        data.append((company, price, deskripsi))
    except Exception as e:
        print(f"Gagal mengambil konten dari {url}: {str(e)}")

# Simpan data dalam format CSV
def save_data_to_excel(data):
    workbook = xlsxwriter.Workbook('Saham 2024.xlsx')
    worksheet = workbook.add_worksheet()

    # Judul dari data
    header_titles = ['Company', 'Price', 'Description']

    # Menulis judul ke sel berbeda di baris pertama
    for col, title in enumerate(header_titles):
        worksheet.write(0, col, title)

    # Menulis data mulai dari baris kedua
    for row, (company, price, description) in enumerate(data, start=1):
        # Menulis data ke sel yang sesuai
        worksheet.write(row, 0, company)
        worksheet.write(row, 1, price)
        worksheet.write(row, 2, description)

    workbook.close()

# Jalankan fungsi penyimpanan data
save_data_to_excel(data)

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
plt.title('Harga Saham Perusahaan')
plt.gca().invert_yaxis()
plt.show()

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
