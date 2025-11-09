import React, { useState } from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

const Chatbot = () => {
  const [messages, setMessages] = useState([
    {
      text: "👋 Hi Ritika, I'm your AI Interview Assistant! I can discuss your skills, projects, and career goals. What would you like to talk about?",
      isUser: false,
    },
  ]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSend = async () => {
    if (!input.trim()) return;
    const userMessage = { text: input, isUser: true };
    setMessages([...messages, userMessage]);
    setInput("");
    setLoading(true);

    try {
      const res = await fetch("http://127.0.0.1:8000/chatbot/ask", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: input }),
      });

      const data = await res.json();
      setMessages((prev) => [
        ...prev,
        { text: data.response || "⚠️ Couldn't fetch response.", isUser: false },
      ]);
    } catch (err) {
      console.error(err);
      setMessages((prev) => [
        ...prev,
        { text: "❌ Backend not reachable.", isUser: false },
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="chat-container">
      <h2>💼 AI Interview Chat</h2>
      <p>Ask questions about your experience, skills, or let me simulate an interview.</p>

      <div className="chat-card">
        <div className="chat-window">
          {messages.map((msg, i) => (
            <div key={i} className={msg.isUser ? "msg user" : "msg bot"}>
              <ReactMarkdown remarkPlugins={[remarkGfm]}>{msg.text}</ReactMarkdown>
            </div>
          ))}
          {loading && <div className="typing">🤖 Thinking...</div>}
        </div>

        <div className="chat-input-area">
          <input
            type="text"
            placeholder="Ask something or say 'Start mock interview'..."
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && handleSend()}
          />
          <button onClick={handleSend}>Send</button>
        </div>
      </div>
    </div>
  );
};

export default Chatbot;
