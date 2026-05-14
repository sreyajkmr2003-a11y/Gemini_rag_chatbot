import axios from "axios";

const BASE_URL = "http://127.0.0.1:8001";

export const ingestWebsite = async (url) => {

  return await axios.post(
    `${BASE_URL}/ingest`,
    { url }
  );
};

export const ingestPDF = async (file) => {

  const formData = new FormData();

  formData.append("file", file);

  return await axios.post(
    `${BASE_URL}/ingest-pdf`,
    formData,
    {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    }
  );
};

export const askQuestion = async (question) => {

  return await axios.post(
    `${BASE_URL}/chat`,
    { question }
  );
};