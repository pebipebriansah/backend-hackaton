import openai
import os
from dotenv import load_dotenv

# Muat variabel dari .env jika perlu
load_dotenv()

# Konfigurasi untuk Azure OpenAI
openai.api_type = "azure"
openai.api_version = "2024-02-15-preview"  # Pastikan ini sesuai dengan versi di Azure kamu
openai.api_base = os.getenv("AZURE_OPENAI_ENDPOINT")  # Contoh: https://myopenai.openai.azure.com/
openai.api_key = os.getenv("AZURE_OPENAI_KEY")
deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT")  # Misal: "gpt4o-mini-deploy"

def generate_rekomendasi_openai(keluhan: str) -> str:
    prompt = f"""
    Kamu adalah ahli agronomi yang sangat berpengalaman dalam penyakit tanaman cabai.
    Berikan diagnosis dan rekomendasi pengobatan yang akurat berdasarkan keluhan berikut:
    
    Keluhan petani: "{keluhan}"
    
    - Jelaskan kemungkinan penyebabnya secara singkat.
    - Berikan rekomendasi cara mengatasinya dengan bahan alami dan kimia jika perlu.
    - Sertakan tips pencegahan agar penyakit tidak menyebar.
    - Jawaban dalam bahasa Indonesia yang mudah dimengerti petani.

    Contoh keluhan: daun menguning, bercak hitam di daun, tanaman layu, hama thrips, dll.
    """

    try:
        response = openai.ChatCompletion.create(
            engine=deployment_name,  # ← WAJIB pakai "engine" untuk Azure, bukan "model"
            messages=[
                {"role": "system", "content": "Kamu adalah asisten ahli agronomi untuk tanaman cabai."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500,
            temperature=0.7,
            top_p=1
        )
        return response.choices[0].message["content"].strip()

    except Exception as e:
        return f"Terjadi kesalahan saat memproses rekomendasi: {str(e)}"
