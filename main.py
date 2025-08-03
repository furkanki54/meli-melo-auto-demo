from flask import Flask, request, jsonify
import os
from elevenlabs import generate, save
from scene_texts import scene_texts

# API anahtarını burada belirt veya .env dosyasından çekebilirsin
ELEVEN_API_KEY = "sk_b7d751949a4ab42dc2efac51e9b1b39f84a6ef226d702a6c"
os.environ["ELEVEN_API_KEY"] = ELEVEN_API_KEY

# Karakter-Ses ID eşleşmeleri
CHARACTER_VOICES = {
    "meli": "EXAVITQu4vr4xnSDxMaL",  # Yasmin Alves
    "melo": "TxGEqnHWrfWFTfGW9XjX",  # Haven Sands
    "narrator": "pNInz6obpgDQGcFmaJgB"  # Rachel (örnek anlatıcı)
}

# Seslerin kaydedileceği klasör
OUTPUT_DIR = "voices"
os.makedirs(OUTPUT_DIR, exist_ok=True)  # Klasör zaten varsa hata vermez

app = Flask(__name__)

# Sahne bazlı üretim
def generate_voice(character, text, index):
    voice_id = CHARACTER_VOICES.get(character)
    if not voice_id:
        return None

    audio = generate(text=text, voice=voice_id, model="eleven_monolingual_v1")
    filename = f"{OUTPUT_DIR}/{index:02d}_{character}.mp3"
    save(audio, filename)
    return filename

@app.route("/")
def home():
    return "Meli & Melo Voice Generator Aktif"

@app.route("/bulk-generate", methods=["POST"])
def bulk_generate():
    try:
        results = []
        for i, scene in enumerate(scene_texts):
            character = scene["character"]
            text = scene["text"]
            file_path = generate_voice(character, text, i)
            results.append({"scene": i, "character": character, "file": file_path})
        return jsonify({"status": "success", "generated": results})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
