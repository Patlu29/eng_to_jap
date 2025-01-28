from flask import Flask, request, jsonify, send_from_directory
from translator import translate_to_japanese, convert_to_romanji, generate_audio
from flask_cors import CORS
import logging
import os

app = Flask(__name__, static_folder="static")
CORS(app)  # Allow requests from React frontend
logging.basicConfig(level=logging.DEBUG)

# Path to the React build folder
frontend_folder = os.path.join(os.getcwd(), "..", "frontend", "dist")

@app.route("/", defaults={"filename": ""})
@app.route("/<path:filename>")
def index(filename):
    if not filename:
        filename = "index.html"
    return send_from_directory(frontend_folder, filename)

@app.route("/api/translate", methods=["POST"])
def translate():
    logging.debug("Translation request received!")
    data = request.json
    english_text = data.get("english_text", "")
    if not english_text:
        logging.error("No text provided in request!")
        return jsonify({"error": "No text provided"}), 400
    
    try:
        japanese_text = translate_to_japanese(english_text)
        romanji_text = convert_to_romanji(japanese_text)
        audio_path = generate_audio(romanji_text)  # Save the audio file in static folder
        logging.debug(f"Japanese: {japanese_text}, Romanji: {romanji_text}, Audio: {audio_path}")
    except Exception as e:
        logging.error(f"Error during translation or audio generation: {e}")
        return jsonify({"error": "Internal server error"}), 500
    
    return jsonify({
        "japanese_text": japanese_text,
        "romanji_text": romanji_text,
        "audio_path": f"{request.host_url}static/output.mp3"
    })

if __name__ == "__main__":
    app.run(debug=True, port=5000)
