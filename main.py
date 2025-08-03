from flask import Flask, jsonify
from elevenlabs import Voice, VoiceSettings, generate, save, set_api_key
import os

app = Flask(__name__)

# API anahtarını ayarla (gizli tut)
set_api_key("sk_b7d751949a4ab42dc2efac51e9b1b39f84a6ef226d702a6c")

# Ses dosyalarının kaydedileceği klasör
OUTPUT_DIR = "voices"
os.makedirs(OUTPUT_DIR, exist_ok=True)

@app.route("/bulk-generate", methods=["POST"])
def bulk_generate():
    try:
        # Test sahneler (sadece 2 tane örnek)
        scene_texts = {
            "meli": ["Cześć, jestem Meli! Wyruszamy w podróż przez czas!"],
            "melo": ["Cześć! Jestem Melo i jestem gotów na przygodę!"],
            "narrator": ["Witajcie w naszej historii pełnej niespodzianek."]
        }

        voice_ids = {
            "meli": "EXAVITQu4vr4xnSDxMaL",    # Yasmin Alves
            "melo": "MF3mGyEYCl7XYWbV9V6O",    # Haven Sands
            "narrator": "21m00Tcm4TlvDq8ikWAM" # Rachel (örnek anlatıcı)
        }

        for character, lines in scene_texts.items():
            for i, line in enumerate(lines):
                audio = generate(
                    text=line,
                    voice=Voice(
                        voice_id=voice_ids[character],
                        settings=VoiceSettings(stability=0.5, similarity_boost=0.7)
                    ),
                    model="eleven_monolingual_v1"
                )
                filename = f"{character}{i+1}.mp3"
                save(audio, os.path.join(OUTPUT_DIR, filename))

        return jsonify({"status": "success", "message": "Ses dosyaları oluşturuldu."})
    
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
