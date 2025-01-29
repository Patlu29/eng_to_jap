# En-Jap_Translator
This is a full-stack English to Japanese Translator application using:

- React(Vite)(Frontend) – Deployed on Render

- Flask (Backend) – Deployed on Render

- SQLite Database – Stores translations and audio files

- MarianMT Model – Translates English to Japanese

- Pykakasi – Converts Japanese text to Romanji

- gTTS – Generates audio pronunciation


# Features

✅ Translate English text to Japanese using MarianMT Model
✅ Convert Japanese text to Romanji (Latin script)
✅ Generate and store audio pronunciation
✅ Fetch previous translations from SQLite database
✅ Full-stack integration (ReactVite & Flask)
✅ Deployed using Render (Backend & Frontend)

# Installation & Setup

1️⃣ Backend Setup (Flask API)

Prerequisites:

- Install Python (3.8+)

- Install dependencies

    pip install -r requirements.txt

- Run the Backend Server

    python app.py

Flask will start on http://localhost:5000


2️⃣ Frontend Setup (ReactVite)

Prerequisites:

- Install Node.js (14+)

- Install dependencies

    npm install

- Run React Frontend

    npm run dev

Frontend will start on http://localhost:5173


# API Endpoints

➤ POST /api/translate

- Request:

{
  "english_text": "Hello, how are you?"
}

- Response:

{
  "japanese_text": "こんにちは、お元気ですか？",
  "romanji_text": "Konnichiwa, ogenki desu ka?",
  "audio_path": "http://localhost:5000/static/output.mp3"
}

➤ GET /api/translations

- Fetches previous translations from the database.

Response:

{
  "id": 1,
  "english_text": "Hello, how are you?",
  "japanese_text": "こんにちは、お元気ですか？",
  "romanji_text": "Konnichiwa, ogenki desu ka?",
  "audio_path": "http://localhost:5000/static/audio.mp3/1"
}


# Deployment

🚀 Deploy Backend to Render

1. Run npm run build

2. Push your backend code to GitHub

3. Connect the repo to Render

4. Set environment variables if needed


# Tech Stack

- Frontend: React (Vite), Axios

- Backend: Flask, SQLite, Flask-CORS

- Translation Model: MarianMT

- Text Processing: Pykakasi

- Audio Generation: gTTS

Deployment: Render (Backend & Frontend)


# Future Improvements

🔹 Add user authentication (JWT)
🔹 Enhance UI/UX with Material UI or TailwindCSS
🔹 Implement caching for faster translations
🔹 Allow file uploads for bulk translations


# Contributors

👨‍💻 Prakash Rajan – Developer & Maintainer
