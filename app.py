import sys
import os
import json
import requests
import asyncio
import streamlit as st
from faster_whisper import WhisperModel
from groq import Groq
from notion_client import Client
from dotenv import load_dotenv
from pydub import AudioSegment
from pydub.silence import split_on_silence

# 1. Manually bridge the audioop gap for Python 3.13
try:
    import audioop
except ImportError:
    try:
        import audioop_lts as audioop
        sys.modules["audioop"] = audioop
    except ImportError:
        pass 

load_dotenv()

# Setup Clients
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))
notion = Client(auth=os.getenv("NOTION_TOKEN"))

# --- OPTIMIZATION: Cache the model loading ---
@st.cache_resource
def load_faster_whisper_model():
    # compute_type="int8" is the key for speed on CPU
    return WhisperModel("base", device="cpu", compute_type="int8")

st.set_page_config(page_title="Meeting Summarizer", page_icon="🚀")
st.title("🎙️ Meet-Summarizer")
st.markdown("Convert Meeting Transcripts to **Notion Tasks** & **Slack Alerts**.")

def preprocess_audio(input_path, output_path):
    audio = AudioSegment.from_file(input_path)
    audio = audio.set_frame_rate(16000).set_channels(1)

    chunks = split_on_silence(
        audio, 
        min_silence_len=1500, 
        silence_thresh=-40, 
        keep_silence=200
    )

    processed_audio = sum(chunks) if chunks else audio
    processed_audio.export(output_path, format="mp3", bitrate="32k")
    return output_path

uploaded_file = st.file_uploader("Upload Meeting Audio", type=["mp3", "wav", "m4a"])

if uploaded_file:
    with open("temp_raw.mp3", "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    if st.button("Generate Insights"):
        # STEP 1: Optimization
        with st.spinner("⚡ Optimizing Audio (Downsampling & Stripping)..."):
            processed_path = preprocess_audio("temp_raw.mp3", "temp_processed.mp3")

        # STEP 2: Transcription with Faster-Whisper
        with st.spinner("1. Transcribing Audio (Faster-Whisper INT8)..."):
            model = load_faster_whisper_model()
            # beam_size=1 is significantly faster than default 5
            segments, info = model.transcribe(processed_path, beam_size=1)
            
            # Efficiently join segments
            transcript_text = " ".join([segment.text for segment in segments])

        # STEP 3: Groq Analysis
        if transcript_text:
            with st.spinner("2. Analyzing with Groq (Llama 3.1 8B)..."):
                prompt = f"""
                You are a professional Project Manager. Analyze the transcript and return ONLY a JSON object:
                {{
                  "summary": "2-sentence overview.",
                  "key_topics": ["Topic: analysis", "Topic: analysis"],
                  "to_do_list": [{{"task": "desc", "assignee": "name"}}],
                  "conclusion": "Final wrap-up."
                }}
                Transcript: {transcript_text}
                """
                
                completion = groq_client.chat.completions.create(
                    model="llama-3.1-8b-instant", 
                    messages=[{"role": "user", "content": prompt}],
                    response_format={"type": "json_object"}
                )
                data = json.loads(completion.choices[0].message.content)
                
                # --- UI DISPLAY ---
                st.subheader("📝 Meeting Overview")
                st.write(data['summary'])

                st.subheader("📌 Key Topics & Analysis")
                for topic in data['key_topics']:
                    st.markdown(f"* {topic}")

                st.subheader("✅ Action Items (To-Do List)")
                if data['to_do_list']:
                    for item in data['to_do_list']:
                        st.markdown(f"- [ ] **{item['task']}** (Owner: {item['assignee']})")
                else:
                    st.write("No specific tasks assigned.")

                st.subheader("🏁 Conclusion")
                st.info(data['conclusion'])

            # STEP 4: Syncing
            with st.spinner("3. Syncing to Notion & Slack..."):
                # Notion Logic
                children_blocks = [
                    {"object": "block", "type": "heading_2", "heading_2": {"rich_text": [{"text": {"content": "Key Topics"}}]}}
                ]
                for topic in data['key_topics']:
                    children_blocks.append({"object": "block", "type": "bulleted_list_item", "bulleted_list_item": {"rich_text": [{"text": {"content": topic}}]}})
                
                children_blocks.append({"object": "block", "type": "heading_2", "heading_2": {"rich_text": [{"text": {"content": "To-Do List"}}]}})
                for item in data['to_do_list']:
                    children_blocks.append({"object": "block", "type": "to_do", "to_do": {"rich_text": [{"text": {"content": f"{item['task']} (@{item['assignee']})"}}]}})

                notion.pages.create(
                    parent={"database_id": os.getenv("NOTION_DATABASE_ID")},
                    properties={"Name": {"title": [{"text": {"content": "Meet-Summarizer Entry"}}]}},
                    children=children_blocks
                )

                # Slack Logic
                slack_payload = {"text": f"🚀 *Meeting Summary Ready!*\n{data['summary']}\n\n*Conclusion:* {data['conclusion']}"}
                requests.post(os.getenv("SLACK_WEBHOOK_URL"), json=slack_payload)
                
                st.success("Synced Successfully!")
        else:
            st.error("Transcription failed to generate text.")