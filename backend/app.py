from flask import Flask, request, jsonify, send_file, url_for
from translator import translate_to_japanese, convert_to_romanji, generate_audio
from flask_cors import CORS
import logging
import os

app = Flask(__name__)
CORS(app, origins=["https://eng-to-jap.vercel.app", "http://localhost:5173"])  # Add Vercel and local domains
logging.basicConfig(level=logging.DEBUG)

@app.route("/api/translate", methods=["POST"])
def translate():
    logging.debug("Translation request received!")
    data = request.json
    english_text = data.get("english_text", "")
    if not english_text:
        logging.error("No text provided in request!")
        return jsonify({"success": False, "error": "No text provided"}), 400

    try:
        japanese_text = translate_to_japanese(english_text)
        romanji_text = convert_to_romanji(japanese_text)
        generate_audio(romanji_text)
        audio_path = url_for("get_audio", _external=True)  # Generate dynamic URL
    except Exception as e:
        logging.error(f"Error during translation or audio generation: {e}")
        return jsonify({"success": False, "error": "Internal server error"}), 500

    return jsonify({
        "success": True,
        "data": {
            "japanese_text": japanese_text,
            "romanji_text": romanji_text,
            "audio_path": audio_path,
        }
    }), 200

@app.route("/static/output.mp3", methods=["GET"])
def get_audio():
    audio_path = "static/output.mp3"
    if not os.path.exists(audio_path):
        return jsonify({"success": False, "error": "Audio file not found"}), 404
    return send_file(audio_path, mimetype="audio/mpeg", as_attachment=False)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
