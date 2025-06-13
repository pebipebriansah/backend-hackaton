from openai import AzureOpenAI
import os

# Load environment variables
api_key = os.getenv("AZURE_OPENAI_KEY")
endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT")  # Contoh: "pebipebriansah160200-4292"
api_version = "2024-05-01-preview"

# Inisialisasi klien Azure OpenAI
client = AzureOpenAI(
    api_key=api_key,
    azure_endpoint=endpoint,
    api_version=api_version
)

def generate_rekomendasi_openai(keluhan: str) -> str:
    try:
        if not deployment_name:
            raise ValueError("AZURE_OPENAI_DEPLOYMENT tidak ditemukan.")

        # Daftar kata kunci diperluas dengan variasi bahasa lokal/tidak baku
        kata_kunci_valid = [
            # Umum
            "cabai", "cabe", "tanaman", "bibit", "daun", "batang", "akar", "buah",
            # Gejala
            "bintik", "bercak", "keriting", "keritingan", "menguning", "layu", "busuk", "pecah", "kering",
            # Bahasa sehari-hari/tidak baku
            "kuning", "hitam", "item", "lemes", "pucat", "kisut", "gugur", "copot",
            "benyek", "mekar", "melempem", "gembur", "kriting", "klayu", "kekuningan",
            # Bahasa lokal kemungkinan
            "daunna", "kabe", "cak", "cebele", "nguning", "coklatan", "iteman", "potean", "layuan",
            # Kata tanya yang bisa mengandung maksud gejala
            "kenapa", "mengapa", "penyebab", "obat", "gimana", "bagaimana", "sakit",
            # Diagnosa/solusi
            "penyakit", "pengobatan", "penyemprotan", "pestisida", "herbal", "kimia", "vitamin", "fungisida", "insektisida"
        ]

        keluhan_lower = keluhan.lower()

        if not any(kata in keluhan_lower for kata in kata_kunci_valid):
            return "Mohon tuliskan keluhan secara lebih lengkap dan pastikan menyebutkan kondisi atau gejala pada tanaman cabai."

        prompt = f"""
Kamu adalah seorang ahli agronomi khusus tanaman cabai. Tugasmu adalah memberikan analisis dan rekomendasi lengkap berdasarkan keluhan petani, meskipun mereka menggunakan bahasa sehari-hari.

**Jika keluhan tidak terkait dengan tanaman cabai, cukup katakan bahwa kamu tidak bisa membantu. Namun jika keluhan menyebut gejala seperti bintik, keriting, menguning, dll, tetap tanggapi sebagai penyakit cabai.**

Gunakan struktur sebagai berikut TANPA markdown atau simbol aneh:

Nama Penyakit: [Isi]
Penyebab: [Isi]
Pengobatan:
1. [Isi]
2. ...
Pencegahan:
1. [Isi]
2. ...
Obat herbal: [Jika ada]
Obat kimia: [Sebutkan bahan aktif, bukan merk]

Keluhan petani: "{keluhan}"
"""

        response = client.chat.completions.create(
            model=deployment_name,
            messages=[
                {"role": "system", "content": "Kamu adalah ahli penyakit tanaman cabai. Jawablah dengan bahasa sederhana yang mudah dimengerti petani."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1200,
            temperature=0.6
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        return f"Terjadi kesalahan saat memproses rekomendasi: {str(e)}"
