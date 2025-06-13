from openai import AzureOpenAI
import os

# Load environment variables
api_key = os.getenv("AZURE_OPENAI_KEY")
endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT")
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

        # Kata kunci untuk memastikan input relevan
        kata_kunci_valid = [
            "cabai", "cabe", "tanaman", "bibit", "daun", "batang", "akar", "buah",
            "bintik", "bercak", "keriting", "menguning", "layu", "busuk", "pecah", "kering",
            "kuning", "hitam", "item", "lemes", "pucat", "gugur", "copot",
            "benyek", "mekar", "melempem", "gembur", "kriting", "klayu",
            "daunna", "kabe", "cebele", "nguning", "coklatan", "iteman", "potean",
            "kenapa", "mengapa", "penyebab", "obat", "gimana", "bagaimana", "sakit",
            "penyakit", "pengobatan", "penyemprotan", "pestisida", "herbal", "kimia", "vitamin", "fungisida", "insektisida"
        ]

        keluhan_lower = keluhan.lower()

        if not any(kata in keluhan_lower for kata in kata_kunci_valid):
            return "Mohon tuliskan keluhan secara lebih lengkap dan pastikan menyebutkan kondisi atau gejala pada tanaman cabai."

        # Prompt yang sudah diperkuat untuk memaksa struktur lengkap termasuk obat
        prompt = f"""
Kamu adalah seorang ahli pertanian dan agronomi khusus tanaman cabai. Tugasmu adalah menganalisis keluhan petani, meskipun dalam bahasa sehari-hari, dan memberikan diagnosa penyakit serta solusi lengkap.

Jika keluhan tidak terkait cabai, cukup katakan bahwa kamu tidak bisa membantu. Tapi jika keluhan menunjukkan gejala seperti daun keriting, menguning, busuk, dll, anggap sebagai penyakit cabai dan tanggapi secara profesional.

Jawaban kamu HARUS mencakup seluruh bagian berikut secara jelas dan terpisah. Jangan hilangkan bagian apapun. Gunakan bahasa sederhana agar mudah dipahami oleh petani.

Format jawaban (WAJIB SESUAI FORMAT):

Nama Penyakit: [Isi, misalnya Antraknosa]
Penyebab: [Singkat, jelas, misalnya jamur Colletotrichum sp.]
Pengobatan:
1. [Langkah 1]
2. [Langkah 2]
Pencegahan:
1. [Langkah pencegahan 1]
2. [Langkah pencegahan 2]
Obat herbal: [Sebutkan jika ada, jika tidak ada tulis "Tidak tersedia"]
Obat kimia: [Sebutkan bahan aktif pestisida atau fungisida, bukan nama merek dagang]

Keluhan petani: "{keluhan}"
"""

        response = client.chat.completions.create(
            model=deployment_name,
            messages=[
                {"role": "system", "content": "Kamu adalah ahli penyakit tanaman cabai. Jawablah dengan bahasa sederhana dan struktural sesuai format."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=2000,
            temperature=0.5,
            frequency_penalty=0.2,
            presence_penalty=0.2
        )

        jawaban = response.choices[0].message.content.strip()

        # Validasi apakah semua bagian penting ada
        bagian_wajib = ["Nama Penyakit:", "Penyebab:", "Pengobatan:", "Pencegahan:", "Obat herbal:", "Obat kimia:"]
        if not all(bagian in jawaban for bagian in bagian_wajib):
            jawaban += "\n\nCatatan: Jawaban mungkin tidak lengkap. Silakan ulangi atau perjelas keluhan Anda."

        return jawaban

    except Exception as e:
        return f"Terjadi kesalahan saat memproses rekomendasi: {str(e)}"
