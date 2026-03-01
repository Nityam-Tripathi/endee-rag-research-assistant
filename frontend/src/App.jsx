import React, { useState } from "react";

function App() {
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [loading, setLoading] = useState(false);
  const [uploading, setUploading] = useState(false);

  const askQuestion = async () => {
    if (!question.trim()) return;

    setLoading(true);
    setAnswer("");

    try {
      const response = await fetch("http://127.0.0.1:8000/ask", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ question }),
      });

      const data = await response.json();
      setAnswer(data.answer || "No answer received.");
    } catch (error) {
      setAnswer("❌ Something went wrong. Make sure backend is running.");
    }

    setLoading(false);
  };

  const uploadDocument = async (file) => {
  if (!file) return;

  setUploading(true);

  const formData = new FormData();
  formData.append("file", file);

  try {
    const response = await fetch("http://127.0.0.1:8000/upload", {
      method: "POST",
      body: formData,
    });

    if (!response.ok) {
      throw new Error("Upload request failed");
    }

    const data = await response.json();

    console.log("Upload response:", data);

    alert("✅ Document uploaded successfully!");
  } catch (error) {
    console.error("Upload error:", error);
    alert("❌ Upload failed. Check console.");
  }

  setUploading(false);
};

  return (
    <div
      style={{
        minHeight: "100vh",
        background: "linear-gradient(to right, #0f172a, #1e293b)",
        padding: "40px",
        fontFamily: "Arial, sans-serif",
        color: "white",
      }}
    >
      <h1 style={{ fontSize: "36px", marginBottom: "10px" }}>
        🧠 Agentic Research AI
      </h1>
      <p style={{ color: "#94a3b8", marginBottom: "30px" }}>
        Powered by Endee Vector Database + LLM Reasoning
      </p>

      {/* Upload Section */}
      <div
        style={{
          marginBottom: "30px",
          padding: "20px",
          background: "#1e293b",
          borderRadius: "10px",
        }}
      >
        <h3>📄 Upload Document (PDF)</h3>
        <input
          type="file"
          accept=".pdf"
          onChange={(e) => uploadDocument(e.target.files[0])}
          disabled={uploading}
          style={{ marginTop: "10px" }}
        />
        {uploading && <p>Uploading and indexing...</p>}
      </div>

      {/* Question Section */}
      <div style={{ display: "flex", gap: "10px", marginBottom: "20px" }}>
        <input
          type="text"
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          placeholder="Ask a question about your document..."
          style={{
            flex: 1,
            padding: "12px",
            borderRadius: "8px",
            border: "none",
            fontSize: "16px",
          }}
        />
        <button
          onClick={askQuestion}
          disabled={loading}
          style={{
            padding: "12px 20px",
            borderRadius: "8px",
            border: "none",
            background: "#3b82f6",
            color: "white",
            fontWeight: "bold",
            cursor: "pointer",
          }}
        >
          {loading ? "Thinking..." : "Ask"}
        </button>
      </div>

      {/* Answer Section */}
      {answer && (
        <div
          style={{
            background: "#1e293b",
            padding: "20px",
            borderRadius: "10px",
            marginTop: "20px",
          }}
        >
          <h3>📌 Final Answer</h3>
          <p style={{ lineHeight: "1.6", marginTop: "10px" }}>{answer}</p>
        </div>
      )}
    </div>
  );
}

export default App;