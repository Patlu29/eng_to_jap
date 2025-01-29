from flask import Flask, request, jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os
from translator import translate_to_japanese, convert_to_romanji, generate_audio

app = Flask(__name__, static_folder="static")
CORS(app)  # Allow requests from React frontend

# Path to the React build folder
frontend_folder = os.path.join(os.getcwd(), "..", "frontend", "dist")

# SQLite Database configuration
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///translations.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

# Database model for translations
class Translation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    english_text = db.Column(db.String, unique=True, nullable=False)
    japanese_text = db.Column(db.String, nullable=False)
    romanji_text = db.Column(db.String, nullable=False)
    audio_data = db.Column(db.LargeBinary, nullable=False)  # Binary data for audio files

# Create database tables
with app.app_context():
    db.create_all()

# Serve the React frontend
@app.route("/", defaults={"filename": ""})
@app.route("/<path:filename>")
def index(filename):
    if not filename:
        filename = "index.html"
    return send_from_directory(frontend_folder, filename)

# API endpoint for translation
@app.route("/api/translate", methods=["POST"])
def translate():
    data = request.json
    english_text = data.get("english_text", "").strip()
    english_text = english_text.lower()  # Convert to lowercase for better matching
    if not english_text:
        return jsonify({"error": "No text provided"}), 400
    
    # Check if translation already exists in the database
    translation = Translation.query.filter_by(english_text=english_text).first()
    if translation:
        return jsonify({
            "japanese_text": translation.japanese_text,
            "romanji_text": translation.romanji_text,
            "audio_path": f"{request.host_url}api/audio/{translation.id}"
        })
    
    try:
        # Perform translation
        japanese_text = translate_to_japanese(english_text)
        romanji_text = convert_to_romanji(japanese_text)
        audio_data = generate_audio(romanji_text)  # Binary audio data
        
        # Save the translation to the database
        translation = Translation(
            english_text=english_text,
            japanese_text=japanese_text,
            romanji_text=romanji_text,
            audio_data=audio_data,
        )
        db.session.add(translation)
        db.session.commit()

        return jsonify({
            "japanese_text": japanese_text,
            "romanji_text": romanji_text,
            "audio_path": f"{request.host_url}api/audio/{translation.id}"
        })
    except Exception as e:
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500

# API endpoint to fetch audio file from the database
@app.route("/api/audio/<int:translation_id>")
def get_audio(translation_id):
    translation = Translation.query.get(translation_id)
    if not translation:
        return jsonify({"error": "Audio not found"}), 404
    
    # Serve the audio file as a binary response
    return (translation.audio_data, 200, {
        "Content-Type": "audio/mpeg",
        "Content-Disposition": f"attachment; filename=output_{translation_id}.mp3"
    })

# **New API Endpoint**: Fetch previous translations
@app.route("/api/translations", methods=["GET"])
def get_translations():
    english_text = request.args.get("english_text")  # Optional query parameter
    if english_text:
        # Filter translations by English text
        translation = Translation.query.filter_by(english_text=english_text.strip()).first()
        if not translation:
            return jsonify({"error": "Translation not found"}), 404
        return jsonify({
            "id": translation.id,
            "english_text": translation.english_text,
            "japanese_text": translation.japanese_text,
            "romanji_text": translation.romanji_text,
            "audio_path": f"{request.host_url}api/audio/{translation.id}"
        })

    # If no query parameter, return all translations
    translations = Translation.query.all()
    results = [
        {
            "id": translation.id,
            "english_text": translation.english_text,
            "japanese_text": translation.japanese_text,
            "romanji_text": translation.romanji_text,
            "audio_path": f"{request.host_url}api/audio/{translation.id}"
        }
        for translation in translations
    ]
    return jsonify(results)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
