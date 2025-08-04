from flask import Flask, request, jsonify
from generate_scenes import generate_voice
import os

app = Flask(__name__)

@app.route("/bulk-generate", methods=["POST"])
def bulk_generate():
    data = request.get_json()

    if not isinstance(data, list):
        return jsonify({"status": "error", "message": "Data must be a list"}), 400

    output_dir = "voices"
    os.makedirs(output_dir, exist_ok=True)

    file_urls = []

    for idx, scene in enumerate(data, start=1):
        character = scene.get("character")
        text = scene.get("text")

        if not character or not text:
            continue

        filename = f"{idx:02d}_{character}.mp3"
        generate_voice(character, text, filename)

        # ✅ MP3 dosyalarının URL'si burada oluşturuluyor
        file_url = f"https://web-production-c6b3.up.railway.app/static/voices/{filename}"
        file_urls.append({
            "character": character,
            "file_url": file_url
        })

    return jsonify({
        "status": "success",
        "files": file_urls
    })

# ❗ Bu kısmı KALDIR / YORUM SATIRI yap – Railway zaten gunicorn ile çalıştırıyor
# if __name__ == "__main__":
#     app.run(debug=True)
