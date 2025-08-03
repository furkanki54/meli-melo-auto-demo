# main.py

from flask import Flask, jsonify
import os

app = Flask(__name__)

OUTPUT_DIR = "voices"
os.makedirs(OUTPUT_DIR, exist_ok=True)

@app.route("/")
def home():
    return jsonify({"message": "Meli & Melo API çalışıyor."})

@app.route("/bulk-generate", methods=["POST"])
def bulk_generate():
    # Demo ses üretim işlemi burada yapılacak
    return jsonify({"status": "success", "message": "Ses üretimi bu noktada tetiklenecek."})
