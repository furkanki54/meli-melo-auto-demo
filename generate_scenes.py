from elevenlabs import generate, save
from scene_texts import scene_data
import os

OUTPUT_DIR = "voices"
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
        print(f"[HATA] Ses üretilemedi: {character} – {e}")
def generate_all():
    for idx, scene in enumerate(scene_data, start=1):
        character = scene["character"]
        text = scene["text"]
        filename = f"{idx:02d}_{character}.mp3"
        generate_voice(character, text, filename)
