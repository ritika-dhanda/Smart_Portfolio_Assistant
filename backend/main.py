import sys
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# ✅ Flexible import system (works locally + on Render)
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

try:
    # Try local (root-level) import
    from backend.routes import chatbot, upload_resume
except ModuleNotFoundError:
    # Fallback for Render (when already inside /backend)
    from routes import chatbot, upload_resume

# ✅ Initialize app
app = FastAPI(title="Smart Portfolio Assistant API")

# ✅ CORS setup (for your frontend on Vercel)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # you can restrict later to your Vercel domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Include routes
app.include_router(chatbot.router)
app.include_router(upload_resume.router)

# ✅ Health check endpoint
@app.get("/health")
def health():
    return {"status": "ok", "message": "Smart Portfolio Assistant backend is running!"}
