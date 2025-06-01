import os
from openai import AzureOpenAI
from dotenv import load_dotenv

load_dotenv()  # pastikan file .env terbaca

# Inisialisasi client khusus Azure
client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_KEY"),
    api_version="2024-02-15-preview",
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
)

# Deployment ID harus string dan tidak None!
deployment_id = os.getenv("AZURE_OPENAI_DEPLOYMENT")

def generate_rekomendasi_openai(keluhan: str) -> str:
    prompt = f"""
    Kamu adalah ahli agronomi yang sangat berpengalaman dalam penyakit tanaman cabai.
    Berikan diagnosis dan rekomendasi pengobatan yang akurat berdasarkan keluhan berikut:

    Keluhan petani: "{keluhan}"

    - Jelaskan kemungkinan penyebabnya secara singkat.
    - Berikan rekomendasi cara mengatasinya dengan bahan alami dan kimia jika perlu.
    - Sertakan tips pencegahan agar penyakit tidak menyebar.
    - Jawaban dalam bahasa Indonesia yang mudah dimengerti petani.
    """

    try:
        # DEBUG
        print("🔧 Deployment ID:", deployment_id)
        print("🔧 Endpoint:", os.getenv("AZURE_OPENAI_ENDPOINT"))
        print("🔧 Key:", os.getenv("AZURE_OPENAI_KEY")[:5] + "...")
        
        if not deployment_id:
            return "ERROR: deployment_id kosong! Cek variabel AZURE_OPENAI_DEPLOYMENT"

        response = client.chat.completions.create(
            deployment_id=deployment_id,  # WAJIB PAKAI INI UNTUK AZURE
            messages=[
                {"role": "system", "content": "Kamu adalah asisten ahli agronomi untuk tanaman cabai."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500,
            temperature=0.7,
            top_p=1
        )
        return response.choices[0].message.content.strip()

    except Exception as e:
        return f"Terjadi kesalahan saat memproses rekomendasi: {str(e)}"
