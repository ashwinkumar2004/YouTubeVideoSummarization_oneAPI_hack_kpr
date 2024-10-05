Here’s a step-by-step detailed procedure to implement the YouTube Video Summarization project, based on the content from the file you uploaded.

Step 1: Initial Setup
1.1. Install Anaconda (Optional)
Download and install Anaconda from here.
Open Anaconda Prompt or your preferred terminal.
1.2. Create a Virtual Environment Using Conda:
Run the following commands to create and activate a Python virtual environment:
bash
Copy code
conda create -n youtube_summary python=3.10
conda activate youtube_summary
1.3. Install Required Libraries:
Install the necessary libraries using pip:
bash
Copy code
pip install youtube-transcript-api streamlit


Step 2: Setting Up YouTube Transcript API
2.1. Extract Video ID:
Extract the video ID from a YouTube URL using Python’s urlparse module:
python
Copy code
from urllib.parse import urlparse

url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
video_id = urlparse(url).path.split("/")[-1]
2.2. Fetch YouTube Transcript:
Use youtube_transcript_api to fetch the transcript based on the video ID:
python
Copy code
from youtube_transcript_api import YouTubeTranscriptApi

transcript = YouTubeTranscriptApi.get_transcript(video_id)

# Store the transcript in a plain text file
with open("transcript.txt", "w") as f:
    for segment in transcript:
        f.write(segment["text"] + "\n")




Step 3: Summarize Transcript Using Google Generative AI (Gemini Pro)
3.1. Set Up Google Gemini Pro API Key:
Get your API key from Google Generative AI (Gemini Pro) and set it up in your environment:
python
Copy code
import os
gemini.configure(api_key=os.getenv("API_KEY"))
3.2. Summarize Transcript:
Define a prompt and use the Google Gemini API to generate a summary of the transcript:
python
Copy code
prompt = "You are a YouTube video summarizer. Provide a summary in points."

# Assuming `transcript_text` is the full text of the transcript
summary = model.generate_content(transcript_text, prompt=prompt, max_tokens=250)




Step 4: Frontend with Streamlit
4.1. Create a Basic Frontend with Streamlit:
Create a file named app.py for the frontend, where users can input a YouTube URL:
python
Copy code
import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi
from urllib.parse import urlparse

# Title
st.title("YouTube Video Summarizer")

# Input box for YouTube URL
url = st.text_input("Enter YouTube Video URL")

if url:
    video_id = urlparse(url).path.split("/")[-1]

    # Fetch the transcript
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        transcript_text = " ".join([segment["text"] for segment in transcript])

        # Display transcript
        st.subheader("Transcript")
        st.write(transcript_text)

        # Summarize the transcript using Google Gemini (or any other summarization tool)
        summary = model.generate_content(transcript_text)
        st.subheader("Summary")
        st.write(summary)
    except Exception as e:
        st.error(f"Error fetching transcript: {e}")
4.2. Run the Streamlit App:
In your terminal, navigate to the folder where your app.py file is located and run:
bash
Copy code
streamlit run app.py




Step 5: Test the Application
Open the local Streamlit web app (it will launch in your browser).
Input a YouTube URL, and the app will fetch and summarize the video transcript.








-------------------------------------------------
modules:

youtube_transcript_api
streamlit
google-generativeai
python-dotenv
pathlib


--------------------------------------------

keycodes for the package activation:

1.conda create -p venv python==3.10 -y

2.conda activate venv/
