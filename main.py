from flask import Flask, request, jsonify
from generate_scenes import generate_all

app = Flask(__name__)

@app.route("/")
def home():
    return "Meli & Melo Voice Generator Aktif!"

@app.route("/generate", methods=["POST"])
def generate_voice():
    data = request.get_json()
    character = data.get("character")
    text = data.get("text")

    if not character or not text:
        return jsonify({"status": "error", "message": "Eksik veri"}), 400

    try:
        file_url = generate_all(character, text)
        return jsonify({"status": "success", "file_url": file_url}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
