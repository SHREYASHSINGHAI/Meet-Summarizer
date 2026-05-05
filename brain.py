from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key="GROQ_API_KEY")

def analyze_transcript(text):
    prompt = f"""
    Analyze the following meeting transcript. 
    Provide a concise summary and a list of actionable tasks with owners.
    Return ONLY a JSON object with this structure:
    {{
      "summary": "...",
      "tasks": [{"task": "...", "owner": "..."}]
    }}
    Transcript: {text}
    """
    
    completion = client.chat.completions.create(
        model="llama3-8b-8192", # Free and fast
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"}
    )
    return completion.choices[0].message.content