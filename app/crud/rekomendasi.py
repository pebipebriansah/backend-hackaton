import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

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

    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",  # atau model lain yang kamu punya aksesnya
        messages=[
            {"role": "system", "content": "Kamu adalah asisten ahli agronomi untuk tanaman cabai."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=500,
        temperature=0.7,
        top_p=1
    )
    return response.choices[0].message.content.strip()
