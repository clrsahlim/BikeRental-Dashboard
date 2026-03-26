# Bike Rental Dashboard 2011-2012 🚲
Dashboard ini menampilkan analisis data penyewaan sepeda tahun 2011-2012, mencakup tren bulanan, pola per musim, perbandingan pengguna kasual vs terdaftar, serta pola penyewaan per jam pada hari kerja dan hari libur.

## Setup Environment - Anaconda
```
conda create --name main-ds python=3.11
conda activate main-ds
pip install -r requirements.txt
```

## Setup Environment - Shell/Terminal
```
mkdir proyek_analisis_data
cd proyek_analisis_data
pipenv install
pipenv shell
pip install -r requirements.txt
```

## Run Streamlit App
```
streamlit run dashboard.py
```
