def generate_rekomendasi(keluhan: str) -> str:
    keluhan = keluhan.lower()
    if "hama" in keluhan:
        return "Gunakan pestisida nabati seperti daun mimba atau semprotan bawang putih."
    elif "daun menguning" in keluhan or "kuning" in keluhan:
        return "Kemungkinan terkena virus kuning. Gunakan insektisida sistemik dan cabut tanaman terinfeksi."
    elif "bercak" in keluhan:
        return "Gunakan fungisida berbahan aktif mancozeb atau tembaga."
    elif "layu" in keluhan:
        return "Lakukan penyiraman rutin dan periksa kondisi akar, kemungkinan fusarium."
    elif "thrips" in keluhan:
        return "Gunakan perangkap kuning atau semprot abamektin secara berkala."
    else:
        return "Keluhan tidak dikenali secara spesifik. Silakan konsultasi lebih lanjut ke penyuluh pertanian."
