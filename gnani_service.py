import os
from dotenv import load_dotenv
from gnani.stt import GnaniSTTClient

load_dotenv()

def transcribe_audio(audio_file):
    api_key = os.getenv("GNANI_API_KEY")

    if not api_key:
        return "Gnani API key is missing."

    try:
        client = GnaniSTTClient(api_key=api_key)

        result = client.transcribe_bytes(
            audio_file.getvalue(),
            filename=audio_file.name,
            language_code="hi-IN",
            model="prisma-v3.0"
        )

        return result.get("transcript", "Transcript not found.")

    except Exception as e:
        return f"Gnani Error: {e}"