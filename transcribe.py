import whisper

def get_transcript(audio_path):
    print("Transcribing audio... this might take a minute.")
    model = whisper.load_model("base") # 'base' is fast and free
    result = model.transcribe(audio_path)
    return result["text"]

if __name__ == "__main__":
    # Test it with a small mp3 file
    print(get_transcript("meeting.mp3"))