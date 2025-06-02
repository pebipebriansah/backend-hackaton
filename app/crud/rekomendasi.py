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
            model=deployment_name,  # ✅ Gunakan nama deployment dari environment
            messages=[
                {"role": "system", "content": "Kamu adalah ahli agronomi tanaman cabai."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500,
            temperature=0.7
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        return f"Terjadi kesalahan saat memproses rekomendasi: {e}"
