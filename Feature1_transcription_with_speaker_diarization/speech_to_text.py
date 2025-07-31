import os
import json
import wave
from dotenv import load_dotenv

import torch
import whisper
from pyannote.audio import Pipeline

# Load environment variables (e.g. HF_TOKEN)
load_dotenv()

# Device selection: GPU if available, else CPU
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Using device: {device}")

# Load Whisper (large is best for multilingual, but "base" is fast for demo)
model = whisper.load_model("base", device=device)   # Change to "large" for high accuracy

# Load PyAnnote diarization pipeline (use pretrained demo pipeline)
HUGGING_FACE_KEY = os.getenv("HF_TOKEN")
diarization_pipeline = (
    Pipeline.from_pretrained(
        "pyannote/speaker-diarization@2.1",
        use_auth_token=HUGGING_FACE_KEY
    )
    .to(device)
)

AUDIO_FILE = "test.wav"

# Run diarization with pyannote
diarization = diarization_pipeline(AUDIO_FILE)

# Helper to get duration
with wave.open(AUDIO_FILE, "rb") as wav_file:
    duration_sec = wav_file.getnframes() / float(wav_file.getframerate())

# Transcribe audio with Whisper in one go
transcription_raw = model.transcribe(AUDIO_FILE, language=None)

# Map transcript segments (from Whisper) to diarization turns (from pyannote)
result = []
for turn, _, speaker in diarization.itertracks(yield_label=True):
    start_time, end_time = turn.start, turn.end
    segment_text = ""
    for seg in transcription_raw["segments"]:
        if (seg["start"] < end_time) and (seg["end"] > start_time):
            segment_text += seg["text"].strip() + " "
    if segment_text.strip():
        result.append({
            "speaker": speaker,
            "start_time": round(start_time, 2),
            "end_time":   round(end_time,   2),
            "text":       segment_text.strip()
        })

# Output final JSON
output = {"transcription": result}
print(json.dumps(output, indent=2, ensure_ascii=False))
