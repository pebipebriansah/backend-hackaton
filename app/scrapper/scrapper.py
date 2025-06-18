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
        nama = item.get("name", "").lower()
        if "cabe" in nama or "cabai" in nama:
            harga_bulan_ini = item["price"]
            
            # ambil harga bulan lalu dari histori
            histories = item.get("histories", [])
            harga_bulan_lalu = None

            if histories:
                # ambil harga pada minggu lalu (anggap sebagai harga bulan lalu)
                harga_bulan_lalu = histories[0]["price"] if len(histories) > 0 else None

            hasil.append({
                "nama": item["name"],
                "harga_bulan_ini": harga_bulan_ini,
                "harga_bulan_lalu": harga_bulan_lalu,
                "satuan": item["unit"],
                "tanggal": item["date"]
            })

    return hasil
