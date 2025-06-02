from openai import AzureOpenAI
import os

# Load environment variables
api_key = os.getenv("AZURE_OPENAI_KEY")
endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT")  # Contoh: "pebipebriansah160200-4292"
api_version = "2024-05-01-preview"  # ✅ Versi terbaru untuk GPT-4o

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

        # Keyword sederhana untuk validasi keluhan penyakit cabai
        keywords = [
            "cabai", "cabe", "cabai rawit", "tanaman cabai", "daun", "bunga", "buah", "batang", "akar",
            "penyakit", "hama", "jamur", "virus", "bakteri", "thrips", "kutu kebul", "kutu daun", "ulat",
            "kumbang", "wereng", "kutu putih", "embun tepung", "bercak", "bintik", "keriting", "layu",
            "busuk", "kuning", "coklat", "hitam", "bercak hitam", "bercak coklat", "bercak kuning", 
            "bercak putih", "jamur tepung", "jamur akar", "layu fusarium", "layu bakteri", "penyakit virus", 
            "mosaik", "virus kuning", "virus keriting", "penggerek buah", "penggerek batang", "busuk buah", 
            "busuk pangkal batang", "antraknosa", "bercak daun", "daun menguning", "daun keriting", 
            "daun melengkung", "daun bergelombang", "daun mengering", "bercak air basah", "bercak berlendir", 
            "bercak berlubang", "serangan hama", "serangga", "kutu", "ulat grayak", "ulat bulu", "ulat daun", 
            "pengendalian hama", "insektisida", "fungisida", "pestisida", "pengobatan tanaman", "gejala penyakit",
            "penyebaran penyakit", "kerusakan daun", "tanaman terserang", "pertumbuhan terganggu", "tanaman layu", 
            "tanaman mati", "tanaman sakit", "gejala serangan hama", "serangan kutu kebul", "serangan thrips"
        ]

        keluhan_lower = keluhan.lower()

        # Cek apakah setidaknya ada satu keyword dalam keluhan
        if not any(keyword in keluhan_lower for keyword in keywords):
            return "Mohon maaf, sistem hanya dapat memberikan rekomendasi untuk penyakit cabai."

        prompt = f"""
        Kamu adalah ahli agronomi. Jawablah keluhan petani di bawah ini dengan format yang jelas dan terstruktur sebagai berikut:

        Nama Penyakit: ...
        Penyebab: ...
        Pengobatan: ...
        Pencegahan: ...

        Keluhan petani: "{keluhan}"

        Jawaban harus dalam bahasa Indonesia dan mudah dimengerti petani.
        """

        response = client.chat.completions.create(
            model=deployment_name,
            messages=[
                {"role": "system", "content": "Kamu adalah ahli agronomi tanaman cabai."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1000,
            temperature=0.7
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        return f"Terjadi kesalahan saat memproses rekomendasi: {e}"

