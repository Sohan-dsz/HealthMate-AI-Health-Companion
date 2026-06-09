# if you dont use pipenv uncomment the following:
from dotenv import load_dotenv
load_dotenv()


import os
from gtts import gTTS
import elevenlabs
from elevenlabs.client import ElevenLabs
from pydub import AudioSegment
import wave
import io
import pyttsx3

ELEVENLABS_API_KEY = os.environ.get("ELEVENLABS_API_KEY")

import subprocess
import platform

def text_to_speech_with_gtts(input_text, output_filepath):
    # Use pyttsx3 for WAV output directly
    engine = pyttsx3.init()
    engine.save_to_file(input_text, output_filepath)
    engine.runAndWait()


input_text="Heloo"
#ext_to_speech_with_gtts(input_text=input_text, output_filepath="gtts_testing_autoplay.mp3")


def text_to_speech_with_elevenlabs(input_text, output_filepath):
    client = ElevenLabs(api_key=ELEVENLABS_API_KEY)
    try:
        audio = client.text_to_speech.convert(
            voice_id="pNInz6obpgDQGcFmaJgB",  # Aria voice ID
            optimize_streaming_latency="0",
            output_format="pcm_22050",  # Change to PCM for WAV conversion
            text=input_text,
            model_id="eleven_turbo_v2",
            voice_settings={
                "stability": 0.1,
                "similarity_boost": 0.3,
                "style": 0.2,
            }
        )

        # Collect audio data
        audio_data = b""
        for chunk in audio:
            audio_data += chunk

        # Convert PCM to WAV
        audio_segment = AudioSegment.from_raw(io.BytesIO(audio_data), sample_width=2, frame_rate=22050, channels=1)
        audio_segment.export(output_filepath, format="wav")

    except Exception as e:
        print(f"Error with ElevenLabs API: {e}")
        # Fallback to gTTS if ElevenLabs fails
        text_to_speech_with_gtts(input_text, output_filepath)

# Test code removed to prevent execution on import
