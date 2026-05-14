import React from "react";

export default function Sidebar({ url, setUrl, onIngest }) {
  return (
    <div className="sidebar">
      <h2 className="title">⚡ RAG Chatbot</h2>

      <input
        value={url}
        onChange={(e) => setUrl(e.target.value)}
        placeholder="Enter website URL"
        className="input"
      />

      <button onClick={onIngest} className="button">
        Ingest Website
      </button>
    </div>
  );
}