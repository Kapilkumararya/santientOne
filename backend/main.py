import os
import shutil
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from google import genai
from fastapi.staticfiles import StaticFiles

from ingest import process_image, process_pdf, process_doc, process_video_link
from rag import add_to_vector_store, query_vector_store
from daily_tasks_service import app as daily_tasks_app
from document_narration_service import app as document_narration_app

# ---------------- LOAD ENV ----------------
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

print("API KEY LOADED:", "YES" if api_key else "NO")

if not api_key:
    raise ValueError("No API key found. Please set GEMINI_API_KEY in .env file")


# ---------------- GEMINI CLIENT ----------------
client = genai.Client(api_key=api_key)
print("Gemini client initialized")

# ---------------- FASTAPI ----------------
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

os.makedirs("storage", exist_ok=True)

# Mount the microservices
app.mount("/daily-tasks", daily_tasks_app)
app.mount("/document-narration", document_narration_app)

# Serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")


# ---------------- UPLOAD ----------------
@app.post("/upload")
async def upload_file(
    file: UploadFile = File(None),
    url: str = Form(None),
    type: str = Form(...)
):
    print("\n--- UPLOAD REQUEST RECEIVED ---")

    text_content = ""

    try:
        if url and type == "video":
            print("Processing video URL")
            text_content = process_video_link(url)

        elif file:
            file_path = f"storage/{file.filename}"
            print("Saving file:", file_path)

            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)

            if type == "pdf":
                print("Processing PDF")
                text_content = process_pdf(file_path)
            elif type == "doc":
                print("Processing DOC")
                text_content = process_doc(file_path)
            elif type == "image":
                print("Processing IMAGE")
                text_content = process_image(file_path)

        print("Text extracted length:", len(text_content))

        chunks_added = add_to_vector_store(text_content)
        print("Chunks added to vector DB:", chunks_added)

        return {
            "status": "success",
            "message": f"Added {chunks_added} chunks."
        }

    except Exception as e:
        print("UPLOAD ERROR:", str(e))
        return {"status": "error", "message": str(e)}


# ---------------- CHAT ----------------
@app.post("/chat")
async def chat(query: str = Form(...)):

    print("\n==============================")
    print("CHAT REQUEST RECEIVED")
    print("User Query:", query)

    # 1. Retrieve context from vector DB
    context = query_vector_store(query)
    print("Context retrieved length:", len(context) if context else 0)

    # 2. Build prompt
    if context:
        prompt = f"""
You are a helpful assistant. Answer ONLY using the context below.
If the answer is not present, say "I don't know".

Context:
{context}

Question:
{query}
"""
    else:
        prompt = query

    print("\n--- PROMPT (first 400 chars) ---")
    print(prompt[:400])

    try:
        # Use guaranteed working Gemini model
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )

        print("\n--- RAW GEMINI RESPONSE ---")
        print(response)

        answer = response.text if response and response.text else ""

        print("\nFINAL ANSWER:", answer)

        return {"answer": answer}

    except Exception as e:
        print("GEMINI ERROR:", str(e))
        return {"error": str(e)}


# ---------------- RUN SERVER ----------------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
