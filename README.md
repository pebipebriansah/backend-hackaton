# Aplikasi Backend FastAPI untuk Petani

Aplikasi backend ini dibuat menggunakan FastAPI sebagai REST API server yang terhubung dengan Azure SQL Database.  
Dirancang untuk mendukung aplikasi pengelolaan hasil panen dan integrasi Machine Learning.

## Fitur Utama
- REST API menggunakan FastAPI  
- Koneksi ke Azure SQL Database menggunakan pyodbc  
- Mendukung upload file multipart (misal foto tanaman)  
- Dapat diperluas dengan modul Machine Learning  

## Struktur Folder
- `app/` : kode sumber FastAPI  
- `ml/` : skrip atau modul Machine Learning (misal model training & inference)  
- `venv/` : environment virtual Python  
- `.env` : konfigurasi environment variabel  
- `requirements.txt` : daftar dependency Python  

## Instalasi

1. Clone repository ini  
2. Buat virtual environment dan aktifkan  
   ```bash
   python -m venv venv
   source venv/bin/activate  # di Windows: venv\Scripts\activate
