import { useState } from "react";

export default function ChatBox() {
  const [url, setUrl] = useState("");
  const [question, setQuestion] = useState("");
  const [messages, setMessages] = useState([]);

const API = "http://127.0.0.1:8000";

  const ingest = async () => {
    try {
      console.log("INGEST CLICKED");

    console.log("FETCHING:", `${API}/ingest`);
      const res = await fetch(`${API}/ingest`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ url }),
      });

      const data = await res.json();

      console.log("STATUS:", res.status);
      console.log("RESPONSE:", data);

      if (!res.ok) {
        throw new Error(data.detail || data.message || "Backend error");
      }

      alert("Ingest successful");

    } catch (err) {
      console.error("INGEST ERROR:", err.message);
      alert("INGEST FAILED: " + err.message);
    }
  };

  const ask = async () => {
    if (!question.trim()) return;

    try {
      const res = await fetch(`${API}/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question }),
      });

      const data = await res.json();

      if (!res.ok) {
        throw new Error(data.detail || data.message || "Chat failed");
      }

      setMessages((prev) => [
        ...prev,
        { role: "user", text: question },
        { role: "bot", text: data.answer },
      ]);

      setQuestion("");

    } catch (err) {
      console.error("CHAT ERROR:", err.message);
    }
  };

  return (
    <div className="app">
      <div className="sidebar">
        <h2>RAG Chatbot</h2>

        <input
          placeholder="Enter URL..."
          value={url}
          onChange={(e) => setUrl(e.target.value)}
        />

        <button onClick={ingest}>Ingest</button>
      </div>

      <div className="chat">
        <div className="messages">
          {messages.map((m, i) => (
            <div key={i} className={`msg ${m.role}`}>
              {m.text}
            </div>
          ))}
        </div>

        <div className="inputBox">
          <input
            placeholder="Ask something..."
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && ask()}
          />

          <button onClick={ask}>Send</button>
        </div>
      </div>
    </div>
  );
}