from fastapi import APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import traceback
import os
import pickle
from pathlib import Path
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer, util
from groq import Groq

# ✅ Initialize router
router = APIRouter(prefix="/chatbot", tags=["Chatbot"])

# ✅ Request model for Swagger
class ChatRequest(BaseModel):
    message: str


# ✅ Load environment variables (works from both root & backend)
BASE_DIR = Path(__file__).resolve().parents[1]  # backend/
env_path = BASE_DIR / ".env"
if not env_path.exists():
    env_path = BASE_DIR.parent / ".env"

if env_path.exists():
    load_dotenv(env_path)
    print(f"🔑 Loaded .env from: {env_path}")
else:
    print("⚠️ .env file not found in backend or project root")

# ✅ Initialize embedding model
try:
    embedder = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
    print("✅ Embedding model loaded successfully")
except Exception as e:
    print("❌ Error loading embedding model:", e)
    embedder = None

# ✅ Initialize Groq client
try:
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    MODEL_NAME = os.getenv("MODEL_NAME", "llama-3.3-70b-versatile")

    if not GROQ_API_KEY:
        raise ValueError("GROQ_API_KEY missing in .env")

    client = Groq(api_key=GROQ_API_KEY)
    print("✅ Groq client initialized successfully")
    print(f"🧠 Using model: {MODEL_NAME}")

except Exception as e:
    print("❌ Error initializing Groq client:", e)
    client = None


# ✅ Global chat memory (temporary)
chat_memory = []
MAX_MEMORY = 6  # last 6 exchanges remembered


# ✅ Chatbot endpoint
@router.post("/ask")
async def chatbot_ask(data: ChatRequest):
    """
    Chatbot endpoint that retrieves the most relevant resume context,
    remembers recent messages, and generates professional answers using Groq.
    """
    try:
        user_question = data.message.strip()
        print(f"🗣️ User Question: {user_question}")

        # Basic validation
        if not user_question:
            return JSONResponse(status_code=400, content={"error": "Message cannot be empty"})

        if embedder is None:
            return JSONResponse(status_code=500, content={"error": "Embedding model not loaded"})

        if client is None:
            return JSONResponse(status_code=500, content={"error": "Groq client not initialized"})

        # ✅ Load resume embeddings
        embeddings_path = os.path.join(BASE_DIR, "data", "resume_embeddings.pkl")
        print("🔍 Looking for embeddings at:", embeddings_path)

        if not os.path.exists(embeddings_path):
            return JSONResponse(status_code=400, content={"error": "No embeddings found. Please upload your resume first."})

        with open(embeddings_path, "rb") as f:
            resume_data = pickle.load(f)

        if not isinstance(resume_data, dict) or "embeddings" not in resume_data or "texts" not in resume_data:
            return JSONResponse(status_code=400, content={"error": "Invalid resume embeddings structure."})

        corpus_embeddings = resume_data["embeddings"]
        corpus_texts = [t for t in resume_data["texts"] if isinstance(t, str) and len(t.split()) > 3]

        # ✅ Auto-fix mismatched lengths
        if len(corpus_embeddings) != len(corpus_texts):
            print(f"⚠️ Mismatch: {len(corpus_embeddings)} embeddings vs {len(corpus_texts)} texts. Syncing...")
            min_len = min(len(corpus_embeddings), len(corpus_texts))
            corpus_embeddings = corpus_embeddings[:min_len]
            corpus_texts = corpus_texts[:min_len]

        if len(corpus_embeddings) == 0:
            return JSONResponse(status_code=400, content={"error": "Resume embeddings are empty."})

        # ✅ Compute similarity and boost project-related context
        query_embedding = embedder.encode(user_question, convert_to_tensor=True)
        cos_scores = util.pytorch_cos_sim(query_embedding, corpus_embeddings)[0]
        top_k = min(8, len(corpus_texts))
        top_results = cos_scores.topk(k=top_k)

        boost_keywords = ["project", "developed", "built", "created", "implemented", "designed", "skills", "experience"]
        boosted_contexts = []

        for idx in top_results[1].tolist():
            if idx < len(corpus_texts):  # prevent out-of-range
                text = corpus_texts[idx]
                score = float(cos_scores[idx])
                if any(k.lower() in text.lower() for k in boost_keywords):
                    score += 0.15
                boosted_contexts.append((score, text))

        # Sort by boosted score and take top 4
        boosted_contexts = sorted(boosted_contexts, key=lambda x: x[0], reverse=True)[:4]
        context = "\n".join([c[1] for c in boosted_contexts])
        print("🔍 Selected boosted context:\n", context[:400], "...")

        # ✅ Update conversation memory
        chat_memory.append({"role": "user", "content": user_question})
        if len(chat_memory) > MAX_MEMORY:
            chat_memory.pop(0)

        # ✅ Prepare conversation context with memory + system prompt
        conversation_context = [
            {
                "role": "system",
                "content": (
                    "You are Ritika Dhanda's AI Portfolio Assistant. "
                    "You understand her resume, skills, and projects. "
                    "Answer clearly and professionally. "
                    "If asked about skills or projects, summarize them as bullet points with technologies and outcomes. "
                    "Always sound confident, resume-accurate, and concise."
                ),
            }
        ]

        conversation_context.extend(chat_memory)
        conversation_context.append(
            {
                "role": "user",
                "content": f"Question: {user_question}\n\nResume Context:\n{context}",
            }
        )

        # ✅ Generate contextual response using Groq
        chat_completion = client.chat.completions.create(
            model=MODEL_NAME,
            messages=conversation_context
        )

        answer = chat_completion.choices[0].message.content.strip()
        chat_memory.append({"role": "assistant", "content": answer})

        print("✅ Chatbot Response:", answer[:300], "...")
        return {"response": answer}

    except Exception as e:
        print("🔥 Chatbot Route Error:", e)
        traceback.print_exc()
        return JSONResponse(status_code=500, content={"error": str(e)})
