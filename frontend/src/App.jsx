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
      const response = await axios.post("/api/translate", {
        english_text: englishText,
      });
      console.log("API Response:", response.data);
      setJapaneseText(response.data.japanese_text);
      setRomanjiText(response.data.romanji_text);
      setAudioPath(response.data.audio_path);
    } catch (error) {
      console.error("Error translating text:", error);
      alert("Failed to translate. Please try again.");
    }
  };

  

  return (
    <div style={{ padding: "20px" }}>
      <h1><img src="/text.png" alt="text" className="textimg"/>English to Japanese Translator</h1>
      <form onSubmit={handleTranslate}>
        <textarea
          value={englishText}
          onChange={(e) => setEnglishText(e.target.value)}
          placeholder="Enter English text here...Enter more then 5 word for better translation(max 500 characters)"
          rows="5"
          cols="50"
        />
        <br />
        <button type="submit">Translate</button>
      </form>
      {japaneseText && (
        <div style={{ marginTop: "20px" }}>
          <h2>Translation:</h2>
          <p>
            <strong>Japanese:</strong> {japaneseText}
          </p>
          <p>
            <strong>Romanji:</strong> {romanjiText}
          </p>
          <p><strong>Audio:</strong></p>
          <audio controls>
            <source src={`${audioPath}?t=${Date.now()}`} type="audio/mp3" />
            Your browser does not support the audio element.
          </audio>
          <h5>For another translation refresh the page.</h5>
        </div>
      )}
    </div>
  );
};

export default App;
