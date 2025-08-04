import os

OUTPUT_DIR = "static/voices"
os.makedirs(OUTPUT_DIR, exist_ok=True)

VOICE_MAP = {
    "meli": "Yasmin Alves",
    "melo": "Haven Sands",
    "narrator": "Rachel"
}

def generate_voice(character, text, filename):
    try:
        voice = VOICE_MAP.get(character.lower(), "Rachel")
        print(f"✅ Sahte ses oluşturuluyor: {character} – {text}")
        filepath = os.path.join(OUTPUT_DIR, filename)
        with open(filepath, "wb") as f:
            f.write(b"fake_mp3_audio_data")
    except Exception as e:
        print(f"[HATA] generate_voice hata: {e}")
        raise e
