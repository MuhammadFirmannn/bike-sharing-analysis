# Bike Sharing Analysis Project

## Deskripsi Proyek

Proyek ini melakukan analisis mendalam terhadap dataset Bike Sharing Washington D.C. (2011-2012) untuk menjawab dua pertanyaan bisnis utama:

1. **Bagaimana pola penggunaan sepeda berubah berdasarkan musim, hari kerja, dan kondisi cuaca?**
2. **Apa karakteristik hari-hari dengan permintaan tertinggi dan terendah, dan bagaimana mengoptimalkan distribusi sepeda?**

## Struktur Proyek

bike-sharing-analysis/
├── data/
│   ├── day.csv              # Data agregat harian (731 baris)
│   └── hour.csv             # Data agregat per jam (17,379 baris)
├── dashboard/
│   ├── dashboard.py         # Aplikasi Streamlit interaktif
│   └── main_data.csv        # Data untuk dashboard
├── Proyek_Analisis_Data.ipynb   # Notebook analisis lengkap
├── requirements.txt         # Dependensi Python
└── README.md               # File ini


## Instalasi & Cara Menjalankan

### Prerequisites
- Python 3.8+
- pip atau conda

### Setup Lokal

1. **Clone atau extract repository:**
   
   cd bike-sharing-analysis
  

2. **Buat virtual environment (opsional):**
   
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # atau
   venv\Scripts\activate     # Windows
   

3. **Install dependencies:**
   
   pip install -r requirements.txt
   

4. **Jalankan dashboard Streamlit:**
   
   streamlit run dashboard/dashboard.py
   

Dashboard akan membuka di browser pada `http://localhost:8501`

### Menjalankan Notebook Analisis

jupyter notebook Proyek_Analisis_Data.ipynb

## Fitur Dashboard

Dashboard interaktif yang dibangun dengan Streamlit menyediakan:

### Tab 1: Seasonal Analysis
- Perbandingan pengguna casual vs registered per musim
- Statistik musiman (mean, median, std, min, max)
- Key insights tentang perbedaan musiman

### Tab 2: Daily Pattern
- Analisis hari kerja vs weekend/libur
- Pola penggunaan per hari dalam seminggu
- Insights tentang perbedaan pola harian

### Tab 3: Weather Impact
- Dampak kondisi cuaca terhadap penggunaan
- Korelasi faktor cuaca dengan total pengguna
- Visualisasi temperature, humidity, windspeed

### Tab 4: Demand Optimization
- Statistik peak vs normal vs low demand days
- Karakteristik masing-masing kategori demand
- Rekomendasi aksi untuk optimalisasi operasional
