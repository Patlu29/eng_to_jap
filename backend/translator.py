from transformers import MarianMTModel, MarianTokenizer
import pykakasi
from gtts import gTTS
import io

# Load the pre-trained model and tokenizer
model_name = "Patlu29/eng-jap_trans"
model = MarianMTModel.from_pretrained(model_name)
tokenizer = MarianTokenizer.from_pretrained(model_name)

# Initialize pykakasi for Romanji conversion
kakasi = pykakasi.kakasi()
kakasi.setMode("H", "a")  # Hiragana to ascii
kakasi.setMode("K", "a")  # Katakana to ascii
kakasi.setMode("J", "a")  # Kanji to ascii
kakasi.setMode("s", True)  # Enable word separation
converter = kakasi.getConverter()

def translate_to_japanese(sentence):
    """Translate English sentence to Japanese."""
    inputs = tokenizer(sentence, return_tensors="pt", padding=True, truncation=True)
    outputs = model.generate(**inputs)
    japanese_output = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return japanese_output

def convert_to_romanji(japanese_text):
    """Convert Japanese text to Romanji."""
    return converter.do(japanese_text)

def generate_audio(romanji_text):
    """Generate audio from Romanji text and return it as binary data."""
    audio_buffer = io.BytesIO()
    tts = gTTS(text=romanji_text, lang="ja")
    try:
        tts.write_to_fp(audio_buffer)  # Write audio data to the buffer
    except Exception as e:
        raise Exception(f"Error generating audio: {e}")
    audio_buffer.seek(0)  # Reset buffer pointer
    return audio_buffer.read()  # Return audio data as binary
