import streamlit as st
from bs4 import BeautifulSoup 
import cloudscraper 
import matplotlib.pyplot as plt

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
st.title('Grafik Saham 2024')

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
                    # nama_company = soup1.find('h2', {'class': 'float_lang_base_1 inlineblock'}).text
                    deskripsi = soup1.find('p', {'id': 'profile-fullStory-showhide'}).text
                    # link_website = soup1.find('span', {'class': 'float_lang_base_2.text_align_lang_base_2 dirLtr'}).text
                    # print(f"Nama Perusahaan: {company}")
                    # print(f"Deskripsi Perusahaan: {deskripsi_company}")
                    # print(f"Harga Saham Perusahaan: {price}")
                    # detail.append(deskripsi_company)
            except Exception as r:
                print(f"Gagal mengambil konten dari {profile_url}: {str(r)}")
        data.append((company, price, deskripsi))
    except Exception as e:
        print(f"Gagal mengambil konten dari {url}: {str(e)}")

# Memisahkan data perusahaan dan harga saham menjadi dua list terpisah (Contoh: ['Nike Inc (NKE)', '92.15'] menjadi [Nike Inc (NKE)], [92.15])
companies, prices, descriptions = zip(*data)

# Ubah harga saham menjadi tipe numerik (hilangkan simbol '$' dan ubah ke float)
prices = [float(price.strip('$')) for price in prices]

# Plot grafik
plt.figure(figsize=(10, 6))
plt.barh(companies, prices, color='#398bff')
plt.xlabel('Harga Saham ($)')
plt.ylabel('Perusahaan')
plt.title('Grafik Saham Perusahaan 2024')
plt.gca().invert_yaxis() 
st.pyplot(plt)

# Judul aplikasi
st.title('Detail Perusahaan')

# Pilih saham dari dropdown
selected_stock = st.selectbox('Pilih Saham:', companies)

# Temukan indeks saham yang dipilih di daftar perusahaan
index = companies.index(selected_stock)

# Tampilkan detail perusahaan yang dipilih
st.write(f'Nama Perusahaan: {companies[index]}')
st.write(f'Harga Saham: ${prices[index]}')
st.write(f'Deskripsi Perusahaan:')
st.write(descriptions[index])
