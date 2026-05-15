import React from "react";

export default function Sidebar({
  url,
  setUrl,
  onIngestUrl,
  onUploadPdf,
}) {
  return (
    <div className="sidebar">

      <h2 className="title">⚡ Multi-Source RAG Chatbot</h2>

      <div className="section">
        <h3>🌐 Website</h3>

        <input
          value={url}
          onChange={(e) => setUrl(e.target.value)}
          placeholder="Enter website URL"
          className="input"
        />

        <button onClick={onIngestUrl} className="button">
          Ingest Website
        </button>
      </div>

      <div className="section">
        <h3>📄 PDF Upload</h3>

        <input
          type="file"
          accept=".pdf"
          onChange={onUploadPdf}
          className="file-input"
        />
      </div>

    </div>
  );
}