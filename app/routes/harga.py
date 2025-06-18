from fastapi import APIRouter, HTTPException
from app.schemas.harga import HargaCabaiResponse, HargaCabai
import requests

router = APIRouter()

@router.get("/", response_model=HargaCabaiResponse, summary="Ambil data harga cabai terbaru")
def get_harga_cabai():
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
        "User-Agent": "Mozilla/5.0 (compatible; HackathonPetaniApp/1.0)",
        "Accept": "application/json"
    }

    try:
        response = requests.get(url, params=params, headers=headers, timeout=10)
        response.raise_for_status()
        json_data = response.json()
    except requests.exceptions.HTTPError as http_err:
        raise HTTPException(status_code=response.status_code, detail=f"❌ HTTP Error: {http_err}")
    except requests.exceptions.RequestException as req_err:
        raise HTTPException(status_code=500, detail=f"❌ Request Error: {req_err}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"❌ Gagal mengambil data: {e}")

    hasil = []
    for item in json_data.get("data", []):
        nama = item.get("name", "").lower()

        if "cabai" in nama or "cabe" in nama:
            try:
                hasil.append(HargaCabai(
                    nama=item.get("name", "-"),
                    harga=int(item.get("price", 0)),
                    satuan=item.get("unit", "kg"),
                    kategori=item.get("categories", "-"),
                    tanggal=item.get("date", "-")
                ))
            except Exception as e:
                print(f"⚠️ Gagal parsing item: {e}")
                continue

    if not hasil:
        raise HTTPException(status_code=404, detail="❌ Data cabai tidak ditemukan.")

    return HargaCabaiResponse(data=hasil)
