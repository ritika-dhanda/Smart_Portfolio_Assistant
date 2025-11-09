import React, { useState } from "react";
import Chatbot from "./Chatbot";
import { MessageCircle, X } from "lucide-react"; // pretty icons

const ChatWidget = () => {
  const [open, setOpen] = useState(false);

  return (
    <div>
      {/* Floating button */}
      {!open && (
        <button
          onClick={() => setOpen(true)}
          style={{
            position: "fixed",
            bottom: "30px",
            right: "30px",
            backgroundColor: "#007bff",
            color: "white",
            border: "none",
            borderRadius: "50%",
            width: "60px",
            height: "60px",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            boxShadow: "0px 4px 10px rgba(0,0,0,0.3)",
            cursor: "pointer",
          }}
        >
          <MessageCircle size={28} />
        </button>
      )}

      {/* Chat window */}
      {open && (
        <div
          style={{
            position: "fixed",
            bottom: "100px",
            right: "30px",
            width: "350px",
            height: "500px",
            backgroundColor: "white",
            border: "1px solid #ccc",
            borderRadius: "12px",
            boxShadow: "0 5px 20px rgba(0,0,0,0.2)",
            display: "flex",
            flexDirection: "column",
            zIndex: 1000,
          }}
        >
          <div
            style={{
              background: "#007bff",
              color: "white",
              padding: "10px",
              borderTopLeftRadius: "12px",
              borderTopRightRadius: "12px",
              display: "flex",
              justifyContent: "space-between",
              alignItems: "center",
            }}
          >
            <span>💬 Smart Portfolio Assistant</span>
            <button
              onClick={() => setOpen(false)}
              style={{
                background: "transparent",
                border: "none",
                color: "white",
                cursor: "pointer",
              }}
            >
              <X size={20} />
            </button>
          </div>

          <div style={{ flex: 1, overflow: "hidden" }}>
            <Chatbot />
          </div>
        </div>
      )}
    </div>
  );
};

export default ChatWidget;
