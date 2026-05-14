# Gemini RAG Chatbot

## Project Title and Description

Gemini RAG Chatbot is an AI-powered question-answering system built using Retrieval-Augmented Generation (RAG).  
It allows users to enter a website URL, processes the content, and answers questions based on the extracted information using Google’s Gemini API.

The system combines semantic search with large language model capabilities to provide accurate, context-aware responses.

---

## Setup and Usage Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/sreyajkmr2003-a11y/Gemini_rag_chatbot.git
cd Gemini_rag_chatbot
```

---

### 2. Backend Setup (FastAPI)

```bash
cd backend
```

Create virtual environment:

```bash
python -m venv venv
```

Activate it:

**Windows**
```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create `.env` file:

```env
GOOGLE_API_KEY=your_api_key_here
```

Run backend server:

```bash
uvicorn main:app --reload
```

---

### 3. Frontend Setup (React)

```bash
cd frontend
npm install
npm start
```

---

### 4. Usage

1. Open the frontend in browser
2. Enter a website URL
3. Click **Ingest**
4. Ask questions based on the website content
5. Get AI-generated responses

---

## Dependencies and Prerequisites

### Backend Dependencies
- FastAPI
- Uvicorn
- FAISS
- Sentence Transformers
- LangChain
- Google Generative AI (Gemini API)
- BeautifulSoup / Web scraping libraries

### Frontend Dependencies
- React
- Axios
- Node.js

### Prerequisites
- Python 3.9+
- Node.js 16+
- Git
- Google Gemini API key

---

## Solution Approach

This project uses a **Retrieval-Augmented Generation (RAG)** architecture.

### Workflow:

1. User submits a website URL
2. Website content is scraped and extracted
3. Text is split into smaller chunks
4. Each chunk is converted into embeddings
5. Embeddings are stored in a FAISS vector database
6. User question is converted into an embedding
7. Similar chunks are retrieved from FAISS
8. Retrieved context is passed to Gemini API
9. Gemini generates a final contextual response

---

## Deployment

- Frontend: Vercel  
- Backend: Render  

Live Demo:
https://gemini-rag-chatbot-czpg.vercel.app/

---

## Author

Sreya
