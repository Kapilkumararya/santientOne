import os
import pytesseract
from PIL import Image
from pypdf import PdfReader
from docx import Document
import yt_dlp
import whisper

# 1. Image OCR (Offline)
def process_image(image_path):
    # Ensure Tesseract is installed on your system
    image = Image.open(image_path)
    text = pytesseract.image_to_string(image)
    return text

# 2. PDF Parsing (Offline)
def process_pdf(pdf_path):
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text

# 3. DOCX Parsing (Offline)
def process_doc(doc_path):
    doc = Document(doc_path)
    text = "\n".join([para.text for para in doc.paragraphs])
    return text

# 4. Video Link -> Audio -> Text (Offline Whisper)
def process_video_link(url, output_folder="storage"):
    # A. Download Audio using yt-dlp
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{'key': 'FFmpegExtractAudio','preferredcodec': 'mp3','preferredquality': '192'}],
        'outtmpl': f'{output_folder}/%(id)s.%(ext)s',
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info).replace(".webm", ".mp3").replace(".m4a", ".mp3")
    
    # B. Transcribe locally using Whisper (Base model is fast and decent)
    model = whisper.load_model("base") 
    result = model.transcribe(filename)
    
    return result["text"]