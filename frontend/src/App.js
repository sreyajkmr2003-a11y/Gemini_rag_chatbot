import { useState } from "react";
import "./App.css";

export default function App() {
  const API = "http://YOUR_IP_OR_DEPLOYED_URL:8000";

  const [url, setUrl] = useState("");
  const [question, setQuestion] = useState("");
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleIngest = async () => {
    if (!url) {
      alert("Please enter a URL");
      return;
    }

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
        throw new Error(data.detail || "Ingest failed");
      }

      alert("Website ingestion successful!");

    } catch (err) {
      console.error(err);
      alert(err.message);

    } finally {
      setLoading(false);
    }
  };

  const handlePdfUpload = async (e) => {
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
        throw new Error(data.detail || "PDF ingest failed");
      }

      alert("PDF ingestion successful!");

    } catch (err) {
      console.error(err);
      alert(err.message);

    } finally {
      setLoading(false);
    }
  };

  const handleAsk = async () => {
    if (!question.trim()) return;

    const userMessage = {
      role: "user",
      text: question,
    };

    setMessages((prev) => [...prev, userMessage]);

    try {
      setLoading(true);

      const res = await fetch(`${API}/chat`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          question,
        }),
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
      console.error(err);
      alert(err.message);

    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="App">

      <div className="sidebar">

        <h1 className="title">
          ⚡ RAG Chatbot
        </h1>

        <div className="section">

          <h3>🌐 Website</h3>

          <input
            type="text"
            placeholder="Enter website URL"
            value={url}
            onChange={(e) => setUrl(e.target.value)}
            className="input"
          />

          <button
            onClick={handleIngest}
            className="button"
          >
            Ingest Website
          </button>
        </div>

        <div className="section">

          <h3>📄 Upload PDF</h3>

          <input
            type="file"
            accept=".pdf"
            onChange={handlePdfUpload}
            className="file-input"
          />
        </div>

      </div>

      <div className="chat-container">

        <div className="chat-header">
          AI Assistant
        </div>

        <div className="messages">

          {messages.map((msg, index) => (
            <div
              key={index}
              className={`message ${
                msg.role === "user"
                  ? "user-message"
                  : "bot-message"
              }`}
            >
              {msg.text}
            </div>
          ))}

          {loading && (
            <div className="bot-message message">
              Thinking...
            </div>
          )}
        </div>

        <div className="chat-input-container">

          <input
            type="text"
            placeholder="Ask a question..."
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            className="chat-input"
          />

          <button
            onClick={handleAsk}
            className="button"
          >
            Send
          </button>

        </div>

      </div>

    </div>
  );
}