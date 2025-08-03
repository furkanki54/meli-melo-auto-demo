import os
import requests
from flask import Flask, request, jsonify, send_from_directory
from scene_texts import scene_texts

app = Flask(__name__)

# ElevenLabs API Key
ELEVEN_API_KEY = os.getenv("ELEVEN_API_KEY", "YOUR_ELEVEN_API_KEY_HERE")
HEADERS = {
    "xi-api-key": ELEVEN_API_KEY,
    "Content-Type": "application/json"
}

VOICE_MAP = {
    "meli": "EXAVITQu4vr4xnSDxMaL",  # Yasmin Alves
    "melo": "MF3mGyEYCl7XYWbV9V6O",   # Haven Sands
    "narrator": "21m00Tcm4TlvDq8ikWAM"  # Rachel (örnek anlatıcı)
}

OUTPUT_DIR = "voices"
os.makedirs(OUTPUT_DIR, exist_ok=True)

@app.route("/")
def home():
    return "Meli & Melo Voice Generator Çalışıyor!"

@app.route("/generate", methods=["POST"])
def generate():
    data = request.json
    text = data.get("text")
    character = data.get("character", "meli").lower()

    if not text or character not in VOICE_MAP:
        return jsonify({"error": "Eksik veri veya geçersiz karakter adı."}), 400

    voice_id = VOICE_MAP[character]
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"

    payload = {
        "text": text,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {
            "stability": 0.4,
            "similarity_boost": 0.7
        }
    }

    response = requests.post(url, headers=HEADERS, json=payload)

    if response.status_code != 200:
        return jsonify({"error": "ElevenLabs API hatası", "status": response.status_code}), 500

    index = len(os.listdir(OUTPUT_DIR)) + 1
    filename = f"{character}_{index:02}.mp3"
    filepath = os.path.join(OUTPUT_DIR, filename)

    with open(filepath, "wb") as f:
        f.write(response.content)

    return jsonify({"message": "Ses üretildi", "file": f"/voices/{filename}"}), 200

@app.route("/bulk-generate", methods=["POST"])
def bulk_generate():
    results = []

    for i, scene in enumerate(scene_texts, start=1):
        character = scene["character"]
        text = scene["text"]

        voice_id = VOICE_MAP[character]
        url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"

        payload = {
            "text": text,
            "model_id": "eleven_multilingual_v2",
            "voice_settings": {
                "stability": 0.4,
                "similarity_boost": 0.7
            }
        }

        response = requests.post(url, headers=HEADERS, json=payload)

        if response.status_code == 200:
            filename = f"{character}_{i:02}.mp3"
            filepath = os.path.join(OUTPUT_DIR, filename)
            with open(filepath, "wb") as f:
                f.write(response.content)
            results.append(f"/voices/{filename}")
        else:
            results.append(f"[HATA] Sahne {i} ({character}): {response.status_code}")

    return jsonify({"message": "İşlem tamamlandı", "dosyalar": results})

@app.route("/voices/<filename>")
def get_voice(filename):
    return send_from_directory(OUTPUT_DIR, filename)

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
