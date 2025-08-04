from elevenlabs import generate, save
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
        audio = generate(text=text, voice=voice, model="eleven_multilingual_v2")
        filepath = os.path.join(OUTPUT_DIR, filename)
        save(audio, filepath)
    except Exception as e:
        print(f"[HATA] generate_voice hata: {e}")
        raise e
