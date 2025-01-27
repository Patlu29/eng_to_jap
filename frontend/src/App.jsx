import React, { useState } from "react";
import axios from "axios";

const App = () => {
  const [englishText, setEnglishText] = useState("");
  const [japaneseText, setJapaneseText] = useState("");
  const [romanjiText, setRomanjiText] = useState("");
  const [audioPath, setAudioPath] = useState("");

  const handleTranslate = async (e) => {
    e.preventDefault();
    try {
      const baseURL =
        window.location.hostname === "localhost"
          ? "http://127.0.0.1:5000/api" // Local backend
          : "https://eng-to-jap.onrender.com/api"; // Production backend

      const response = await axios.post(`${baseURL}/translate`, {
        english_text: englishText,
      });
      console.log("API Response:", response.data);
      setJapaneseText(response.data.data.japanese_text);
      setRomanjiText(response.data.data.romanji_text);
      setAudioPath(response.data.data.audio_path);
    } catch (error) {
      console.error("Error translating text:", error);
      alert("Failed to translate. Please try again.");
    }
  };

  return (
    <div style={{ padding: "20px" }}>
      <h1>English to Japanese Translator</h1>
      <form onSubmit={handleTranslate}>
        <textarea
          value={englishText}
          onChange={(e) => setEnglishText(e.target.value)}
          placeholder="Enter English text here...Enter max(5 words) for better results😁"
          rows="5"
          cols="50"
        />
        <br />
        <button type="submit">Translate</button>
      </form>
      {japaneseText && (
        <div style={{ marginTop: "20px" }}>
          <h2>Translation:</h2>
          <p><strong>Japanese:</strong> {japaneseText}</p>
          <p><strong>Romanji:</strong> {romanjiText}</p>
          <p><strong>Audio:</strong></p>
          <audio controls>
            <source src={`${audioPath}?t=${Date.now()}`} type="audio/mp3" />
            Your browser does not support the audio element.
          </audio>
        </div>
      )}
    </div>
  );
};

export default App;
