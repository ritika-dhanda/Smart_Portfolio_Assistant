import { useState } from "react";
import Chatbot from "./components/Chatbot";
import ResumeUpload from "./components/ResumeUpload";
import "./index.css";

function App() {
  const [page, setPage] = useState("upload");

  return (
    <div className="interview-app">
      <header className="app-header">
        <h1>🤖 Smart Portfolio Interview Assistant</h1>
        <p>
          Your <strong>AI-powered career companion</strong> — ready to analyze your
          resume, discuss your achievements, and help you shine in interviews 💼
        </p>
      </header>

      <div className="nav-bar">
        <button
          className={page === "upload" ? "nav-btn active" : "nav-btn"}
          onClick={() => setPage("upload")}
        >
          📄 Upload Resume
        </button>
        <button
          className={page === "chat" ? "nav-btn active" : "nav-btn"}
          onClick={() => setPage("chat")}
        >
          💬 Interview Chat
        </button>
      </div>

      <div className="main-card">
        {page === "upload" ? <ResumeUpload /> : <Chatbot />}
      </div>

      <footer className="footer">
        Built by <strong>Ritika Dhanda</strong> 🧠 | Powered by <strong>Groq AI</strong>
      </footer>
    </div>
  );
}

export default App;
