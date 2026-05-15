import React from "react";

export default function Sidebar({
  url,
  setUrl,
  onIngestUrl,
  onUploadPdf,
}) {

  return (
    <div className="w-full sm:w-80 h-full p-4 bg-gray-900 text-white flex flex-col gap-6">

      <h2 className="text-xl font-bold">
        ⚡ Multi-Source RAG Chatbot
      </h2>

      {/* WEBSITE INGEST */}
      <div className="flex flex-col gap-2">

        <h3 className="font-semibold">🌐 Website</h3>

        <input
          value={url}
          onChange={(e) => setUrl(e.target.value)}
          placeholder="Enter website URL"
          className="p-2 rounded text-black"
        />

        <button
          onClick={onIngestUrl}
          className="bg-blue-600 hover:bg-blue-700 p-2 rounded"
        >
          Ingest Website
        </button>
      </div>

      {/* PDF INGEST */}
      <div className="flex flex-col gap-2">

        <h3 className="font-semibold">📄 PDF Upload</h3>

        <input
          type="file"
          accept=".pdf"
          onChange={onUploadPdf}
          className="text-sm"
        />

      </div>

    </div>
  );
}