from flask import Flask, request
from generate_scenes import generate_all
import os

app = Flask(__name__)

# Seslerin kaydedileceği klasör
OUTPUT_DIR = "voices"
os.makedirs(OUTPUT_DIR, exist_ok=True)

@app.route("/")
def home():
    return "✅ Meli & Melo Ses Üretim Sistemi Aktif!"

@app.route("/bulk-generate", methods=["GET", "POST"])
def bulk_generate():
    if request.method == "GET":
        return "🔄 Bu endpoint POST isteği ile çalışır. Lütfen POST atınız."
    
    try:
        generate_all()
        return "🎉 Ses dosyaları başarıyla üretildi!"
    except Exception as e:
        return f"❌ Hata oluştu: {str(e)}"

if __name__ == "__main__":
    app.run(debug=True)
