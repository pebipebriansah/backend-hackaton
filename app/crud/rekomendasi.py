from openai import AzureOpenAI
import os

# Pastikan ini tidak None
client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_KEY"),
    api_version="2024-02-15-preview",
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
)

deployment_id = os.getenv("AZURE_OPENAI_DEPLOYMENT")
model_name = "gpt-4o-mini"  # Replace with your actual model name

def generate_rekomendasi_openai(keluhan: str) -> str:
    try:
        if not deployment_id:
            raise ValueError("AZURE_OPENAI_DEPLOYMENT tidak ditemukan.")

        prompt = f"""
        Kamu adalah ahli agronomi yang sangat berpengalaman dalam penyakit tanaman cabai.
        Berikan diagnosis dan rekomendasi pengobatan yang akurat berdasarkan keluhan berikut:

        Keluhan petani: "{keluhan}"

        - Jelaskan kemungkinan penyebabnya secara singkat.
        - Berikan rekomendasi cara mengatasinya dengan bahan alami dan kimia jika perlu.
        - Sertakan tips pencegahan agar penyakit tidak menyebar.
        - Jawaban dalam bahasa Indonesia yang mudah dimengerti petani.
        """

        response = client.chat.completions.create(
            deployment_id=deployment_id,
            model=model_name,  # Add the model parameter
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