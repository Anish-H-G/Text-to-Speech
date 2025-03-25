from flask import Flask, render_template, request, jsonify
import os
import io
from dotenv import load_dotenv
from pydub import AudioSegment
import azure.cognitiveservices.speech as speechsdk

app = Flask(__name__)

load_dotenv()

# Azure Speech Configuration
api_key = os.getenv('api_key')
region = os.getenv('region')

speech_config = speechsdk.SpeechConfig(subscription=api_key, region=region)
speech_config.speech_synthesis_voice_name = 'en-IN-AashiNeural'

def synthesize_speech(text):
    """Convert text to speech and return audio as bytes without saving to a file."""
    audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)
    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)
    
    result = speech_synthesizer.speak_text_async(text).get()
    
    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        return result.audio_data  # Return audio bytes
    return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/synthesize', methods=['POST'])
def synthesize():
    """Handle text-to-speech conversion request."""
    try:
        text = request.form.get('text')
        if not text:
            return jsonify({"error": "No text provided"}), 400
       
        audio_file = synthesize_speech(text)
        if audio_file:
            return jsonify({"audio_file":"/"+ audio_file.hex()})
        
        return jsonify({"error": "Text-to-speech conversion failed"}),500
    
    except Exception as e:
       return jsonify({"error": str(e)}), 500 

if __name__ == '__main__':
    app.run(debug=True)