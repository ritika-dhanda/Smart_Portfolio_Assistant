# 🤖 Smart Portfolio Interview Assistant

**Smart Portfolio Interview Assistant** is an AI-powered resume chatbot that reads a candidate's resume, answers questions about skills and projects, and can run a *Mock Interview Mode* to help job seekers practice for technical interviews.

Built with **FastAPI** (backend), **Sentence-Transformers** (embeddings), **Groq LLM** (Llama 3.3 model), and **React + Vite** (frontend).

## Features

- ✅ Upload a PDF resume and extract text automatically.
- ✅ Create and store resume embeddings for fast retrieval.
- ✅ Ask natural language questions about your resume (skills, projects, experience).
- ✅ **Mock Interview Mode** — the assistant asks interview-style questions based on your resume and gives feedback.
- ✅ Conversation memory for contextual follow-ups.
- ✅ Markdown-formatted responses for clear, readable output.
- ✅ Modern, polished UI suitable for portfolio demos.

---

## Tech Stack

- **Frontend:** React, Vite, react-markdown, remark-gfm  
- **Backend:** FastAPI, Uvicorn  
- **Embeddings:** `sentence-transformers` (all-MiniLM-L6-v2)  
- **LLM:** Groq (Llama 3.3 via Groq API)  
- **Storage:** Local filesystem for resume embeddings (can be swapped for DB/IPFS)

---

## Project Structure

```
smart_portfolio/
├── backend/
│   ├── data/                         # resume_embeddings.pkl (generated)
│   ├── routes/
│   │   ├── chatbot.py
│   │   └── upload_resume.py
│   ├── main.py
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Chatbot.jsx
│   │   │   └── ResumeUpload.jsx
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   └── index.css
│   ├── package.json
│   └── vite.config.js
├── .gitignore
└── README.md
```

---

## Quickstart (Local)

> Make sure you have Python 3.10+ and Node.js installed.

### Backend

1. Create and activate a virtual environment (recommended inside backend folder):
```bash
cd backend
python -m venv .venv
# Windows (PowerShell)
.venv\Scripts\Activate.ps1
# macOS / Linux
source .venv/bin/activate
```

2. Install backend deps:
```bash
pip install -r requirements.txt
```

3. Create `.env` (copy from `.env.example`) and set:
```
GROQ_API_KEY=your_groq_api_key_here
MODEL_NAME=llama-3.3-70b-versatile
FRONTEND_URL=http://localhost:5173
```

4. Run backend:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Backend Swagger: `http://127.0.0.1:8000/docs`

---

### Frontend

1. In a new terminal:
```bash
cd frontend
npm install
```

2. Start dev server:
```bash
npm run dev
```

Open: `http://localhost:5173`

**Flow:** Upload resume on Upload page → embeddings are created → switch to Chat page → ask questions or start Mock Interview.

---

## Mock Interview Mode (how it works)

- The assistant analyzes your resume for technical topics and picks a set of interview-style questions (behavioral + technical).
- Mode behaviour (from the UI): send message `Start mock interview` or press the “Start mock interview” button (if included). The assistant:
  1. Asks 4–8 questions tailored to resume items.
  2. Waits for your answer (you type).
  3. Gives feedback: correctness, tips, suggested talking points, and sample improved answers.
- Use for practice and to generate bullet points for talking about projects.

---

## API Endpoints (important)

- `POST /resume/upload` — Upload resume PDF (`file` form field). Generates `backend/data/resume_embeddings.pkl`.
- `POST /chatbot/ask` — Body: `{ "message": "..." }`. Returns `{ "response": "..." }`.

---

## Deployment (short summary)

1. **Backend (Render)**: create a Web Service pointing to `backend/` — `pip install -r requirements.txt` and start `uvicorn main:app --host 0.0.0.0 --port 10000`. Add env vars in Render (GROQ_API_KEY, MODEL_NAME, FRONTEND_URL).
2. **Frontend (Vercel)**: point to `frontend/`, build command `npm run build`, output `dist`. Add `VITE_API_BASE` env var pointing to Render backend URL.

See the **Deployment** section later in this README for step-by-step instructions.

---

## Environment Variables

**Backend `.env`**
```
GROQ_API_KEY=...
MODEL_NAME=llama-3.3-70b-versatile
FRONTEND_URL=http://localhost:5173
```

**Frontend `.env`** (optional, used if you reference `VITE_API_BASE`):
```
VITE_API_BASE=http://localhost:8000
```

> Never commit real API keys — add `.env` to `.gitignore`.

---

## Development Tips

- If responses seem generic, re-upload the resume to refresh embeddings.
- For reproducible environments, create `requirements.txt` from your virtualenv via `pip freeze > requirements.txt`.
- To debug CORS issues: ensure `FRONTEND_URL` is in backend CORS allow list or set `allow_origins=["*"]` while developing.


## Screenshots

![alt text](image-1.png)
![alt text](image.png)

## Live Demo

## License

MIT © Ritika Dhanda

---

## Contact

Ritika Dhanda — RITIKA_21BCS8217 — [LinkedIn](#) • [GitHub](#)
