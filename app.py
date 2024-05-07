from bs4 import BeautifulSoup 
import cloudscraper 
import matplotlib.pyplot as plt

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
 
# Buat objek scraper
scraper = cloudscraper.create_scraper(delay=10, browser="chrome")

# List untuk menyimpan hasil(company, price) dari setiap URL
data = []

# Loop melalui setiap URL dan ambil kontennya
for url in urls:
    try:
        # Ambil konten dari URL saat ini
        content = scraper.get(url).text
        soup = BeautifulSoup(content,'html.parser') 
        company = soup.find('h1', {'class':'mb-2.5 text-left text-xl font-bold leading-7 text-[#232526] md:mb-2 md:text-3xl md:leading-8 rtl:soft-ltr'}).text
        price = soup.find('div', {'class':'text-5xl/9 font-bold text-[#232526] md:text-[42px] md:leading-[60px]'}).text 
        data.append((company, price))
    except Exception as e:
        print(f"Gagal mengambil konten dari {url}: {str(e)}")

# Memisahkan data perusahaan dan harga saham menjadi dua list terpisah (Contoh: ['Nike Inc (NKE)', '92.15'] menjadi [Nike Inc (NKE)], [92.15])
companies, prices = zip(*data)

# Ubah harga saham menjadi tipe numerik (hilangkan simbol '$' dan ubah ke float)
prices = [float(price.strip('$')) for price in prices]

# Plot grafik
plt.figure(figsize=(10, 6))
plt.barh(companies, prices, color='#398bff')
plt.xlabel('Harga Saham ($)')
plt.ylabel('Perusahaan')
plt.title('Harga Saham Perusahaan')
plt.gca().invert_yaxis()
plt.show()
