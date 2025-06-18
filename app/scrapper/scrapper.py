# scraper.py

import requests

def ambil_harga_cabai():
    url = "https://data.jabarprov.go.id/api-dashboard-jabar/public/pangan/list-komoditas"
    params = {
        "kota": 21,        # Majalengka
        "pasar": 373,      # Pasar Kadipaten
        "search": "",
        "page": 1,
        "limit": 100,
        "order": "asc",
        "order_by": "name"
    }

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, params=params, headers=headers)
    data = response.json()

    hasil = []
    for item in data.get("data", []):
        hasil.append({
            "nama": item["name"],
            "harga": item["price"],
            "satuan": item["unit"],
            "kategori": item["categories"],
            "tanggal": item["date"]
        })

    return hasil
