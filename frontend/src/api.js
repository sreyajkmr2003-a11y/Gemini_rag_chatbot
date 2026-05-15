import axios from "axios";

// ❌ NEVER use localhost for mobile apps
const BASE_URL = "http://YOUR_IP_OR_DEPLOYED_URL:8001";

// -----------------------------
// INGEST WEBSITE
// -----------------------------
export const ingestWebsite = async (url) => {
  return await axios.post(`${BASE_URL}/ingest`, { url });
};


// -----------------------------
// INGEST PDF
// -----------------------------
export const ingestPDF = async (file) => {
  const formData = new FormData();
  formData.append("file", file);

  return await axios.post(`${BASE_URL}/ingest-pdf`, formData, {
    headers: {
      "Content-Type": "multipart/form-data",
    },
  });
};


// -----------------------------
// CHAT QUESTION
// -----------------------------
export const askQuestion = async (question) => {
  return await axios.post(`${BASE_URL}/chat`, { question });
};