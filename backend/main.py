from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from backend.routes import chatbot, upload_resume
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI(title="Smart Portfolio Backend")

# ✅ CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Register routers
app.include_router(upload_resume.router)
app.include_router(chatbot.router)

@app.get("/")
def root():
    return {"message": "Backend is live 🚀"}
