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

    try:
        response = requests.get(url, params=params, headers=headers, timeout=10)
        response.raise_for_status()
        json_data = response.json()
    except Exception as e:
        print(f"❌ Error saat mengambil data: {e}")
        return []

    hasil = []
    for item in json_data.get("data", []):
        nama = item.get("name", "").lower()
        
        # Ambil hanya yang mengandung kata "cabai" atau "cabe"
        if "cabai" in nama or "cabe" in nama:
            try:
                hasil.append({
                    "nama": item["name"],
                    "harga": int(item["price"]),
                    "satuan": item.get("unit", "kg"),
                    "tanggal": item.get("date", ""),
                    "gambar": item.get("url", "")
                })
            except Exception as e:
                print(f"⚠️ Gagal parsing item {item.get('name', 'Unknown')}: {e}")
                continue

    return hasil
