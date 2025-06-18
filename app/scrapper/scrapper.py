import requests

def ambil_harga_cabai():
    url = "https://data.jabarprov.go.id/api-dashboard-jabar/public/pangan/list-komoditas"
    params = {
        "kota": 21,
        "pasar": 373,
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
            histories = item.get("histories", [])
            harga_bulan_lalu = histories[0]["price"] if histories else None

            hasil.append({
                "nama": item["name"],
                "harga_bulan_ini": harga_bulan_ini,
                "harga_bulan_lalu": harga_bulan_lalu,
                "satuan": item["unit"],
                "tanggal": item["date"]
            })

    return hasil

# Tampilkan hasil ke console
if __name__ == "__main__":
    hasil = ambil_harga_cabai()
    for data in hasil:
        print(data)
