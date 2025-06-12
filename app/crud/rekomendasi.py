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

        if not any(keyword in keluhan_lower for keyword in keywords):
            return "Mohon maaf, sistem hanya dapat memberikan rekomendasi untuk penyakit cabai."

        prompt = f"""
Anda adalah seorang ahli agronomi tanaman cabai. Tugas Anda adalah membantu petani cabai dengan menjawab keluhan mereka secara jelas, lengkap, dan mudah dimengerti.

Jawaban harus disusun dengan struktur berikut, TANPA menggunakan format markdown, simbol seperti bintang (**), garis miring, atau tanda pagar (#):

Nama Penyakit: [tuliskan nama penyakit jika diketahui]
Penyebab: [jelaskan penyebab atau penyebaran penyakit tersebut]
Pengobatan:
1. [Langkah pertama pengobatan]
2. [Langkah kedua pengobatan]
dst...

Pencegahan:
1. [Langkah pertama pencegahan]
2. [Langkah kedua pencegahan]
dst...

Berikan juga informasi tambahan berikut:
- Obat herbal alami yang bisa digunakan oleh petani sebagai alternatif pengendalian hama atau penyakit, lengkap dengan cara membuat dan cara aplikasinya jika memungkinkan.
- Jenis bahan kimia (insektisida atau fungisida) yang umum digunakan di Indonesia untuk kasus tersebut, sebutkan juga nama bahan aktifnya dan waktu aplikasi yang tepat.

Jawaban harus dalam bahasa Indonesia yang sederhana dan bisa dipahami oleh petani.

Keluhan petani: "{keluhan}"
"""

        response = client.chat.completions.create(
            model=deployment_name,
            messages=[
                {"role": "system", "content": "Anda adalah ahli agronomi tanaman cabai yang bertugas membantu petani dengan rekomendasi praktis dan mudah dipahami."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1200,
            temperature=0.7
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        return f"Terjadi kesalahan saat memproses rekomendasi: {e}"


