from openai import OpenAI
import os

# Load environment variables
api_key = os.getenv("OPENROUTER_API_KEY")  # API key dari OpenRouter.ai
base_url = "https://openrouter.ai/api/v1"  # Endpoint OpenRouter

# Inisialisasi klien OpenAI dengan OpenRouter base_url
client = OpenAI(api_key=api_key, base_url=base_url)

def generate_rekomendasi_openai(keluhan: str) -> str:
    try:
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
Kamu adalah seorang ahli pertanian dan agronomi khusus tanaman cabai.  
Tugasmu adalah menganalisis keluhan petani, yang mungkin disampaikan dengan bahasa sehari-hari, dan memberikan diagnosa penyakit serta solusi lengkap.

Berikan jawaban yang SANGAT TERSTRUKTUR dan JELAS dengan bahasa yang sederhana agar mudah dipahami petani.

**BATASAN:**  
- Fokus hanya pada tanaman cabai dan gejala-gejala yang umum terjadi pada tanaman cabai.  
- Jika keluhan tidak terkait cabai, jawab dengan kalimat sopan bahwa kamu tidak dapat membantu.

**Format jawaban WAJIB ikuti persis seperti ini:**  
Nama Penyakit: [nama penyakit singkat]  
Penyebab: [penyebab utama singkat, jelas]  
Pengobatan:  
1. [langkah pengobatan 1]  
2. [langkah pengobatan 2]  
...  
Pencegahan:  
1. [langkah pencegahan 1]  
2. [langkah pencegahan 2]  
...  
Obat herbal: [jika ada sebutkan, jika tidak tulis "Tidak tersedia"]  
Obat kimia: [sebutkan bahan aktif pestisida/fungisida, jangan merek dagang]

**Catatan penting:**  
- Jika tidak ada data untuk salah satu bagian, tuliskan "Tidak tersedia" pada bagian tersebut, jangan dikosongkan.  
- Gunakan poin-poin untuk pengobatan dan pencegahan agar mudah dibaca.  
- Jangan menambahkan informasi di luar format yang diminta.  
- Jawaban harus lengkap dan jangan melewatkan bagian apapun.

**Contoh jawaban:**  
Nama Penyakit: Antraknosa  
Penyebab: Jamur Colletotrichum sp.  
Pengobatan:  
1. Semprot dengan fungisida berbahan aktif mancozeb.  
2. Buang dan musnahkan bagian tanaman yang terinfeksi.  
Pencegahan:  
1. Hindari penyiraman pada daun agar daun tetap kering.  
2. Rotasi tanaman dengan tanaman non-solanaceae.  
Obat herbal: Ekstrak daun mimba.  
Obat kimia: Mancozeb, Tebuconazole.

Keluhan petani: "{keluhan}"
"""

        response = client.chat.completions.create(
            model="deepseek-chat",  # Ganti sesuai model OpenRouter yang kamu pakai
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
