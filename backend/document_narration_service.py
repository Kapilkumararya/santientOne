from fastapi import FastAPI, UploadFile
from pypdf import PdfReader
from docx import Document
from fastapi.middleware.cors import CORSMiddleware
from gtts import gTTS
import os

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/narrate_pdf")
async def narrate_pdf(file: UploadFile):
    # Logic to narrate PDF with chaptering and TTS
    pdf_reader = PdfReader(file.file)
    chapters = []
    audio_files = []

    for i, page in enumerate(pdf_reader.pages):
        text = page.extract_text()
        chapters.append(text)

        # Generate audio for each chapter
        tts = gTTS(text)
        # Save audio files in the static/audio directory
        audio_dir = "static/audio"
        os.makedirs(audio_dir, exist_ok=True)
        audio_file = os.path.join(audio_dir, f"chapter_{i + 1}.mp3")
        tts.save(audio_file)
        audio_files.append(audio_file)

    return {"chapters": chapters, "audio_files": audio_files}

@app.post("/narrate_docx")
async def narrate_docx(file: UploadFile):
    # Logic to narrate DOCX with chaptering and TTS
    doc = Document(file.file)
    chapters = [p.text for p in doc.paragraphs if p.text.strip()]
    audio_files = []

    for i, text in enumerate(chapters):
        # Generate audio for each chapter
        tts = gTTS(text)
        # Save audio files in the static/audio directory
        audio_dir = "static/audio"
        os.makedirs(audio_dir, exist_ok=True)
        audio_file = os.path.join(audio_dir, f"chapter_{i + 1}.mp3")
        tts.save(audio_file)
        audio_files.append(audio_file)

    return {"chapters": chapters, "audio_files": audio_files}