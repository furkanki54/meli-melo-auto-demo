import os
from flask import Flask, request, jsonify
from scene_texts import scene_texts

app = Flask(__name__)

OUTPUT_DIR = "voices"

# Klasör varsa hata vermez
try:
    os.makedirs(OUTPUT_DIR, exist_ok=True)
except FileExistsError:
    pass

@app.route("/bulk-generate", methods=["POST"])
def bulk_generate():
    results = []
    for i, scene in enumerate(scene_texts, 1):
        character = scene["character"]
        text = scene["text"]

        filename = f"{OUTPUT_DIR}/scene_{i:02d}_{character}.txt"
        try:
            with open(filename, "w", encoding="utf-8") as f:
                f.write(f"{character.upper()}: {text}")
            results.append(f"[OK] Sahne {i} yazıldı: {filename}")
        except Exception as e:
            results.append(f"[HATA] Sahne {i} yazılamadı: {str(e)}")

    return jsonify({
        "message": "Tüm sahneler işlendi.",
        "results": results
    })

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
