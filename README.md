# DarwixAI_Assessment

This repository contains two main features:

1. **Audio Diarization & Transcription Script** – a standalone Python script that performs speaker diarization (via PyAnnote) and transcription (via Whisper).
2. **Blog Title Suggestion Service** – a Django REST API that generates three blog post title suggestions using OpenAI (or Deepseek).


---

## Prerequisites

- **Python:** 3.8 or higher
- **FFmpeg CLI:** Required for audio processing
  - **Ubuntu/Debian:** `sudo apt-get install ffmpeg`
  - **macOS (Homebrew):** `brew install ffmpeg`
- **Git** (to clone the repo)

---

## Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/Hritesh1001/DarwixAI_Assessment.git
   cd DarwixAI_Assessment
   ```

2. **Create and activate a virtual environment**

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**

   ```bash
   pip3 install -r requirements.txt
   ```

---

## Configuration

1. **Create a '.env' file** in the project root:

   ```ini
   # OpenAI / Deepseek
   OPENAI_API_KEY=<your-deepseek-key>

   # Hugging Face (for pyannote)
   HF_TOKEN=<your-huggingface-token>
   ```

---

## FEATURE-1: Audio Diarization & Transcription

1. **Ensure your audio file** (e.g., `test.wav`) is in the project root or update the `AUDIO_FILE` constant in `diarize_and_transcribe.py`.

2. **Run the script**

   ```bash
   python3 diarize_and_transcribe.py
   ```

3. **Output** The script will print a JSON object with speaker-labeled segments and their transcriptions, e.g.:

   ```json
   {
     "transcription": [
       {"speaker":"SPEAKER_00","start_time":0.0,"end_time":4.88,"text":"Hello, this is..."},
       {"speaker":"SPEAKER_01","start_time":4.88,"end_time":9.90,"text":"Hi, welcome..."},
       ...
     ]
   }
   ```

---

## FEATURE-2: Blog Title Suggestion Service (Django)

1. **Apply migrations**

   ```bash
   python3 manage.py migrate
   ```

2. **Run the development server**

   ```bash
   python3 manage.py runserver
   ```

3. **Test the endpoint**

   ```bash
   curl -X POST http://127.0.0.1:8000/api/suggest-titles/ \
     -H "Content-Type: application/json" \
     -d '{"content":"In this post we explore the benefits of meditation..."}'
   ```

   **Expected JSON response**:

   ```json
   {
     "titles": [
       "Your First Generated Title",
       "Your Second Generated Title",
       "Your Third Generated Title"
     ]
   }
   ```

---

## Notes & Tips

- **Switching models**: In `blog/title_generator.py`, you can swap `model` or adjust `temperature` to control creativity.
- **Logging**: Add `print` or use Python’s `logging` module to debug.
- **Production**: Consider Dockerizing both components and securing the Django API with authentication and throttling.

---

Thanks a lot for providing me with this opportunity.
I hope you like it.
