from flask import Flask, request, jsonify
import os
import uuid
import requests

app = Flask(__name__)

# STATIC KLASÖRÜ OTOMATİK OLUŞTUR
os.makedirs("static/auto_voices", exist_ok=True)

ELEVENLABS_API_KEY = "sk_b7d751949a4ab42dc2efac51e9b1b39f84a6ef226d702a6c"

VOICE_IDS = {
    "meli": "EXAVITQu4vr4xnSDxMaL",   # Yasmin Alves
    "melo": "MF3mGyEYCl7XYWbV9V6O",   # Haven Sands
    "narrator": "21m00Tcm4TlvDq8ikWAM"  # Rachel (örnek)
}

@app.route("/bulk-generate", methods=["POST"])
def bulk_generate():
    data = request.get_json()
    if not data:
        return jsonify({"status": "error", "message": "JSON eksik."}), 400

    results = []

    for item in data:
        character = item.get("character")
        text = item.get("text")

        if character not in VOICE_IDS:
            return jsonify({"status": "error", "message": f"Geçersiz karakter: {character}"}), 400

        voice_id = VOICE_IDS[character]
        filename = f"{uuid.uuid4().hex}_{character}.mp3"
        filepath = os.path.join("static/auto_voices", filename)

        # ElevenLabs API ile ses üretimi
        response = requests.post(
            f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}",
            headers={
                "xi-api-key": ELEVENLABS_API_KEY,
                "Content-Type": "application/json"
            },
            json={
                "text": text,
                "model_id": "eleven_multilingual_v2",
                "voice_settings": {
                    "stability": 0.4,
                    "similarity_boost": 0.75
                }
            }
        )

        if response.status_code != 200:
            return jsonify({
                "status": "error",
                "message": f"Ses üretimi başarısız: {character}",
                "details": response.text
            }), 500

        # MP3 dosyasını yaz
        with open(filepath, "wb") as f:
            f.write(response.content)

        # Linki ekle
        file_url = f"https://{request.host}/static/auto_voices/{filename}"
        results.append({
            "character": character,
            "file_url": file_url
        })

    return jsonify({
        "status": "success",
        "results": results
    })

@app.route("/", methods=["GET"])
def home():
    return "API çalışıyor!"

if __name__ == "__main__":
    app.run(debug=True)
