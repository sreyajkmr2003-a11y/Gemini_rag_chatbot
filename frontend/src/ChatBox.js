import { useState } from "react";

export default function ChatBox() {

  const [url, setUrl] = useState("");
  const [question, setQuestion] = useState("");
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);

  // 🔥 FIXED FOR MOBILE + DEPLOYMENT
 const API = "http://192.168.1.73:10000";


  const ingest = async () => {
    try {
      setLoading(true);

      const res = await fetch(`${API}/ingest`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ url }),
      });

      const data = await res.json();

      if (!res.ok) {
        throw new Error(data.detail || "Backend error");
      }

      alert("Website ingestion successful");

    } catch (err) {
      alert("INGEST FAILED: " + err.message);

    } finally {
      setLoading(false);
    }
  };


  const uploadPdf = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    try {
      setLoading(true);

      const formData = new FormData();
      formData.append("file", file);

      const res = await fetch(`${API}/ingest-pdf`, {
        method: "POST",
        body: formData,
      });

      const data = await res.json();

      if (!res.ok) {
        throw new Error(data.detail || "PDF upload failed");
      }

      alert("PDF ingestion successful");

    } catch (err) {
      alert("PDF FAILED: " + err.message);

    } finally {
      setLoading(false);
    }
  };


  const ask = async () => {
    if (!question.trim()) return;

    const userMessage = { role: "user", text: question };

    setMessages((prev) => [...prev, userMessage]);

    try {
      setLoading(true);

      const res = await fetch(`${API}/chat`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ question }),
      });

      const data = await res.json();

      if (!res.ok) {
        throw new Error(data.detail || "Chat failed");
      }

      const botMessage = {
        role: "bot",
        text: data.answer,
      };

      setMessages((prev) => [...prev, botMessage]);
      setQuestion("");

    } catch (err) {
      alert("CHAT ERROR: " + err.message);

    } finally {
      setLoading(false);
    }
  };


  return (
    <div className="app">

      <div className="sidebar">
        <h2>⚡ RAG Chatbot</h2>

        <input
          placeholder="Enter URL..."
          value={url}
          onChange={(e) => setUrl(e.target.value)}
        />

        <button onClick={ingest}>
          Ingest Website
        </button>

        <input
          type="file"
          accept=".pdf"
          onChange={uploadPdf}
        />
      </div>

      <div className="chat">

        <div className="messages">

          {messages.map((m, i) => (
            <div key={i} className={`msg ${m.role}`}>
              {m.text}
            </div>
          ))}

          {loading && (
            <div className="msg bot">
              Thinking...
            </div>
          )}

        </div>

        <div className="inputBox">

          <input
            placeholder="Ask something..."
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && ask()}
          />

          <button onClick={ask}>
            Send
          </button>

        </div>

      </div>

    </div>
  );
}