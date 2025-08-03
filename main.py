from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/generate", methods=["POST"])
def generate():
    data = request.get_json()
    character = data.get("character")
    text = data.get("text")

    # Test için sabit link dönelim
    return jsonify({
        "file_url": f"https://example.com/{character}.mp3"
    })

if __name__ == "__main__":
    app.run(debug=True)
