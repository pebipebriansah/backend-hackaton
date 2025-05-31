import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_rekomendasi_openai(keluhan: str) -> str:
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Kamu adalah asisten rekomendasi pertanian."},
            {"role": "user", "content": f"Berikan solusi untuk keluhan: {keluhan}"}
        ]
    )
    return response.choices[0].message.content.strip()
