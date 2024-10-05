import streamlit as st
from dotenv import load_dotenv
import os
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi
import speech_recognition as sr
import tempfile
from pydub import AudioSegment

load_dotenv()  # Load all the environment variables
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

prompt = """You are a YouTube video summarizer. You will be taking the transcript text
and summarizing the entire video and providing the important summary in points
within 250 words. Please provide the summary of the text given here:  """


# Getting the transcript data from YouTube videos
def extract_transcript_details(youtube_video_url):
    try:
        video_id = youtube_video_url.split("=")[1]
        transcript_text = YouTubeTranscriptApi.get_transcript(video_id)

        transcript = ""
        for i in transcript_text:
            transcript += " " + i["text"]

        return transcript

    except Exception as e:
        raise e


# Getting the summary based on Prompt from Google Gemini Pro
def generate_gemini_content(transcript_text, prompt):
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt + transcript_text)
    return response.text


# Speech recognition function
def recognize_audio(file):
    recognizer = sr.Recognizer()

    # Create a temporary file for the uploaded audio
    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
        tmp_file.write(file.read())
        tmp_file_path = tmp_file.name

    # Convert MP3 to WAV if necessary
    if tmp_file_path.endswith('.mp3'):
        wav_file_path = tmp_file_path.replace('.mp3', '.wav')
        audio_segment = AudioSegment.from_mp3(tmp_file_path)
        audio_segment.export(wav_file_path, format='wav')
        audio_file_path = wav_file_path
    else:
        audio_file_path = tmp_file_path

    try:
        with sr.AudioFile(audio_file_path) as source:
            audio_data = recognizer.record(source)
            text = recognizer.recognize_google(audio_data)
        return text
    except Exception as e:
        st.error(f"Error in audio recognition: {str(e)}")
        return None


st.title("YouTube Transcript to Detailed Notes Converter")

# Input for YouTube link
youtube_link = st.text_input("Enter YouTube Video Link:")

if youtube_link:
    video_id = youtube_link.split("=")[1]
    st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg", use_column_width=True)

if st.button("Get Detailed Notes from YouTube Video"):
    if youtube_link:
        transcript_text = extract_transcript_details(youtube_link)
        if transcript_text:
            summary = generate_gemini_content(transcript_text, prompt)
            st.markdown("## Detailed Notes:")
            st.write(summary)
    else:
        st.warning("Please enter a valid YouTube video link.")


# Input for audio file upload
st.header("Or Upload an Audio File for Transcription")
audio_file = st.file_uploader("Choose an audio file...", type=["wav", "mp3"])

if audio_file and st.button("Get Detailed Notes from Audio"):
    with st.spinner("Recognizing audio..."):
        transcript_text = recognize_audio(audio_file)
        if transcript_text:
            summary = generate_gemini_content(transcript_text, prompt)
            st.markdown("## Detailed Notes:")
            st.write(summary)
