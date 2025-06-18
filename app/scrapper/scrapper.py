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
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        print(f"Error saat mengambil data: {e}")
        return []

    hasil = []
    for item in data.get("data", []):
        nama = item.get("name", "").lower()
        if "cabe" in nama or "cabai" in nama:
            harga_bulan_ini = item.get("price") or 0
            histories = item.get("histories", [])
            harga_bulan_lalu = histories[0]["price"] if histories else 0

            hasil.append({
                "nama": item.get("name", ""),
                "harga_bulan_ini": int(harga_bulan_ini),
                "harga_bulan_lalu": int(harga_bulan_lalu),
                "satuan": item.get("unit", ""),
                "tanggal": item.get("date", "")
            })

    return hasil
