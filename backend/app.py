from flask import Flask, request, jsonify, send_file
from translator import translate_to_japanese, convert_to_romanji, generate_audio
from flask_cors import CORS
import logging
import os

app = Flask(__name__)
CORS(app)  # Allow requests from React frontend
logging.basicConfig(level=logging.DEBUG)

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
        audio_path = generate_audio(romanji_text)
        logging.debug(f"Japanese: {japanese_text}, Romanji: {romanji_text}, Audio: {audio_path}")
    except Exception as e:
        logging.error(f"Error during translation or audio generation: {e}")
        return jsonify({"error": "Internal server error"}), 500
    
    return jsonify({
        "japanese_text": japanese_text,
        "romanji_text": romanji_text,
        "audio_path": f"http://127.0.0.1:5000/static/output.mp3"
    })

@app.route("/static/output.mp3", methods=["GET"])
def get_audio():
    logging.debug("Audio file requested.")
    audio_path = "static/output.mp3"
    if not os.path.exists(audio_path):
        logging.error("Audio file not found!")
        return jsonify({"error": "Audio file not found"}), 404
    return send_file(audio_path, mimetype="audio/mpeg", as_attachment=False)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
