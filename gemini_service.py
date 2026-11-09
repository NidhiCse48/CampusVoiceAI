import os
from dotenv import load_dotenv
from google import genai
from rag_service import retrieve_context

# Load API key from .env
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY not found in .env file")

# Connect Gemini
client = genai.Client(api_key=api_key)


def ask_gemini(question):

    # Retrieve relevant college information
    context = retrieve_context(question)

    prompt = f"""
    You are CampusVoice AI, a helpful college assistant.

    College Information:
    {context}

    Student Question:
    {question}

    Instructions:
    - Answer in simple English, Hindi or Hinglish.
    - Give clear and helpful answers.
    - Use the provided college information.
    - If information is unavailable, clearly say so.
    - Never invent college details.
    """

    response = client.models.generate_content(
        model="gemini-3.8-flash",
        contents=prompt
    )

    return response.text