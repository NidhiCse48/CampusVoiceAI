import os
import streamlit as st
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Load Streamlit Cloud secrets
try:
    for key in ["GEMINI_API_KEY", "GNANI_API_KEY"]:
        if key in st.secrets:
            os.environ[key] = st.secrets[key]
except Exception:
    pass

from gemini_service import ask_gemini
from gnani_service import transcribe_audio

# Page settings
st.set_page_config(
    page_title="CampusVoiceAI",
    page_icon="🎓",
    layout="centered"
)

st.title("🎓 CampusVoiceAI")
st.write("Your AI-powered college assistant")

st.markdown("---")

st.subheader("💬 Ask your question")

question = st.text_input(
    "Type your college-related question:"
)

if st.button("Get Answer"):
    if question.strip():
        try:
            with st.spinner("Thinking..."):
                answer = ask_gemini(question)
            st.success("Answer:")
            st.write(answer)
        except Exception as e:
            st.error(f"Error: {e}")
    else:
        st.warning("Please enter a question.")

st.markdown("---")

st.subheader("🎤 Ask using your voice")

audio_file = st.audio_input("Record your question")

if audio_file:
    st.audio(audio_file)

    if st.button("Convert Voice to Text"):
        with st.spinner("Converting your voice..."):
            transcript = transcribe_audio(audio_file)

        st.write("Your question:")
        st.write(transcript)

        if transcript and not transcript.startswith("Gnani Error"):
            if "not found" not in transcript.lower():
                try:
                    with st.spinner("Getting answer..."):
                        answer = ask_gemini(transcript)

                    st.success("CampusVoiceAI Answer:")
                    st.write(answer)

                except Exception as e:
                    st.error(f"Gemini Error: {e}")

st.markdown("---")
st.caption("CampusVoiceAI | B.P. Mandal College of Engineering")
