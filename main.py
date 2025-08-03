from flask import Flask, request, jsonify
from elevenlabs import generate, save
import os

app = Flask(__name__)

OUTPUT_DIR = "voices"
os.makedirs(OUTPUT_DIR, exist_ok=True)

VOICE_MAP = {
    "meli": "EXAVITQu4vr4xnSDxMaL",
    "melo": "MF3mGyEYCl7XYWbV9V6O",
    "narrator": "TxGEqnHWrfWFTfGW9XjX"
}

@app.route("/generate", methods=["POST"])
def generate_voice():
    data = request.get_json()
    character = data.get("character")
    text = data.get("text")

    if not character or not text:
        return jsonify({"error": "character ve text gereklidir"}), 400

    voice_id = VOICE_MAP.get(character.lower())
    if not voice_id:
        return jsonify({"error": f"Geçersiz karakter: {character}"}), 400

    try:
        audio = generate(text=text, voice=voice_id)
        filename = f"{character}_{text[:10].replace(' ', '_')}.mp3"
        filepath = os.path.join(OUTPUT_DIR, filename)
        save(audio, filepath)
        file_url = f"https://{request.host}/voices/{filename}"
        return jsonify({"file_url": file_url})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/")
def home():
    return "Ses üretim servisi çalışıyor."

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
