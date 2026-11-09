import os
from pathlib import Path
from dotenv import load_dotenv
from gnani.stt import GnaniSTTClient

# Load .env from the project folder
BASE_DIR = Path(__file__).resolve().parent
ENV_PATH = BASE_DIR / ".env"

load_dotenv(dotenv_path=ENV_PATH, override=True)


def transcribe_audio(audio_file):
    api_key = os.getenv("GNANI_API_KEY", "").strip()

    if not api_key:
        raise ValueError(
            "GNANI_API_KEY not found. Please check your .env file."
        )

    # Initialize Gnani Speech-to-Text client
    client = GnaniSTTClient(api_key=api_key)

    # Reset uploaded file position
    audio_file.seek(0)

    # Transcribe Hindi audio using Gnani Prisma
    result = client.transcribe(
        audio_file,
        language_code="hi-IN",
        model="prisma-v3.0"
    )

    transcript = result.get("transcript", "")

    if not transcript:
        raise ValueError("No speech was detected in the audio.")

    return transcript