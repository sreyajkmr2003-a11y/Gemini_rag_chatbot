import { useState } from "react";

export default function App() {
  const [url, setUrl] = useState("");

  const API = "http://localhost:8000";

  const handleIngest = async () => {
    try {
      const res = await fetch(`${API}/ingest`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ url }),
      });

      const data = await res.json();

      console.log("INGEST RESPONSE:", data);

      if (!res.ok) {
        throw new Error(data.detail || "Ingest failed");
      }

      alert("Ingest successful!");

    } catch (err) {
      console.error("INGEST ERROR:", err.message);
      alert(err.message);
    }
  };

  return (
    <div style={{ padding: "20px" }}>
      <h1>RAG Chatbot</h1>

      <input
        type="text"
        placeholder="Enter website URL"
        value={url}
        onChange={(e) => setUrl(e.target.value)}
        style={{
          width: "400px",
          padding: "10px",
          marginRight: "10px",
        }}
      />

      <button onClick={handleIngest}>
        Ingest
      </button>
    </div>
  );
}