import os
from dotenv import load_dotenv
from gnani.stt import GnaniSTTClient

load_dotenv()

def transcribe_audio(audio_file):
    api_key = os.getenv("GNANI_API_KEY")

    if not api_key:
        return "Error: GNANI_API_KEY is missing. Please check Streamlit Secrets."

    try:
        client = GnaniSTTClient(api_key=api_key)

        audio_bytes = audio_file.getvalue()

        result = client.transcribe_bytes(
            audio_bytes,
            filename=audio_file.name,
            language_code="hi-IN",
            model="prisma-v3.0"
        )

        return result.get("transcript", "No transcript received.")

    except Exception as e:
        return f"Gnani transcription error: {str(e)}"