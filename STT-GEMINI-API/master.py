from flask import Flask, request, jsonify
import speech_recognition as sr
import os
from Gemini_API import *

app = Flask(__name__)
r = sr.Recognizer()

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if not file.filename.endswith('.wav'):
        return jsonify({"error": "Invalid file format, only .wav allowed"}), 400

    audio_path = 'audio.wav'
    file.save(audio_path)

    try:
        with sr.AudioFile(audio_path) as source:
            audio_data = r.record(source)
            text = r.recognize_google(audio_data)
            gemini = generate(text)
            return jsonify({"Speech": text,"transcription": gemini}), 200
    except sr.UnknownValueError:
        return jsonify({"error": "Could not understand audio"}), 400
    except sr.RequestError as e:
        return jsonify({"error": f"Speech recognition service error: {e}"}), 500
    except Exception as e:
        return jsonify({"error": f"Server error: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
