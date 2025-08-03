from flask import Flask, request, jsonify
from elevenlabs import generate, save
import os

app = Flask(__name__)

# Ses dosyalarının kaydedileceği klasör
OUTPUT_DIR = "voices"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Karakterlere göre voice ID ve name eşlemesi
VOICE_MAP = {
    "meli": {"voice_id": "EXAVITQu4vr4xnSDxMaL", "file_prefix": "meli"},
    "melo": {"voice_id": "ErXwobaYiN019PkySvjV", "file_prefix": "melo"},
    "narrator": {"voice_id": "21m00Tcm4TlvDq8ikWAM", "file_prefix": "narrator"}
}

# Basit demo sahneleri
SCENE_TEXTS = {
    "meli": [
        "Cześć, jestem Meli! Wyruszamy w podróż przez czas!",
        "Patrz Melo! To są dinozaury! Niesamowite!"
    ],
    "melo": [
        "Hej Meli! To miejsce wygląda niesamowicie!",
        "Uciekajmy! Ten tyranozaur wygląda groźnie!"
    ],
    "narrator": [
        "Meli i Melo otwierają magiczne drzwi czasu i trafiają do ery dinozaurów."
    ]
}

@app.route("/bulk-generate", methods=["POST"])
def generate_all():
    try:
        for character, scenes in SCENE_TEXTS.items():
            voice_id = VOICE_MAP[character]["voice_id"]
            prefix = VOICE_MAP[character]["file_prefix"]

            for i, text in enumerate(scenes, start=1):
                audio = generate(text=text, voice=voice_id)
                filename = os.path.join(OUTPUT_DIR, f"{prefix}{i}.mp3")
                save(audio, filename)

        return jsonify({"status": "success", "message": "Ses dosyaları başarıyla üretildi."})
    
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
