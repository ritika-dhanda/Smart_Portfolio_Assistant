from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse
import os
import pickle
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from PyPDF2 import PdfReader

router = APIRouter(prefix="/resume", tags=["Resume"])

load_dotenv()

# Initialize embedding model once
embedder = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")


@router.post("/upload")
async def upload_resume(file: UploadFile = File(...)):
    try:
        print("📄 Received resume file:", file.filename)

        # Save the uploaded resume temporarily
        resume_dir = os.path.join(os.path.dirname(__file__), "..", "data")
        resume_dir = os.path.abspath(resume_dir)
        os.makedirs(resume_dir, exist_ok=True)

        resume_path = os.path.join(resume_dir, file.filename)
        with open(resume_path, "wb") as f:
            f.write(await file.read())

        # Extract text from PDF
        reader = PdfReader(resume_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""

        if not text.strip():
            return JSONResponse(status_code=400, content={"error": "Could not extract text from resume."})

        # Split text into chunks for embeddings
        sentences = [s.strip() for s in text.split("\n") if s.strip()]
        embeddings = embedder.encode(sentences, convert_to_tensor=True)

        # Save embeddings for chatbot
        embeddings_data = {
            "texts": sentences,
            "embeddings": embeddings
        }

        embeddings_path = os.path.join(resume_dir, "resume_embeddings.pkl")
        with open(embeddings_path, "wb") as f:
            pickle.dump(embeddings_data, f)

        print("✅ Resume embeddings saved at:", embeddings_path)

        return {"message": "Resume uploaded and embeddings saved successfully."}

    except Exception as e:
        print("🔥 Resume Upload Error:", e)
        return JSONResponse(status_code=500, content={"error": str(e)})
