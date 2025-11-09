import React, { useState } from "react";

const ResumeUpload = () => {
  const [file, setFile] = useState(null);
  const [message, setMessage] = useState("");

  const handleUpload = async () => {
    if (!file) {
      setMessage("⚠️ Please select a PDF file first.");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await fetch("http://127.0.0.1:8000/resume/upload", {
        method: "POST",
        body: formData,
      });

      const data = await res.json();
      if (res.ok) {
        setMessage("✅ Resume uploaded successfully! You can now start chatting.");
      } else {
        setMessage("❌ Upload failed: " + (data.error || "Unknown error."));
      }
    } catch (err) {
      console.error(err);
      setMessage("❌ Server error: Could not upload resume.");
    }
  };

  return (
    <div className="upload-container">
      <h2>🗂️ Upload Your Resume</h2>
      <p>Let me analyze your skills and experience to tailor your interview insights.</p>

      <input
        type="file"
        accept=".pdf"
        onChange={(e) => setFile(e.target.files[0])}
      />
      <button onClick={handleUpload}>Upload</button>
      {message && <p className="upload-msg">{message}</p>}
    </div>
  );
};

export default ResumeUpload;
