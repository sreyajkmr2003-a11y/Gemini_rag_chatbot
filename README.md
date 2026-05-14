# Gemini RAG Chatbot

An AI-powered Retrieval-Augmented Generation (RAG) chatbot built using React, FastAPI, FAISS, and Google's Gemini API.

## Features

- Website URL ingestion
- Semantic search
- Context-aware AI responses
- FastAPI backend
- React frontend
- FAISS vector database
- Gemini-powered chatbot

---

## Tech Stack

### Frontend
- React
- Axios
- CSS

### Backend
- FastAPI
- LangChain
- Sentence Transformers
- FAISS
- Gemini API

---

## Project Structure

```bash
Gemini_rag_chatbot/
│
├── backend/
│   ├── main.py
│   ├── requirements.txt
│
├── frontend/
│   ├── src/
│   ├── public/
│
├── .gitignore
├── README.md
```

---

## Installation

### Clone Repository

```bash
git clone https://github.com/sreyajkmr2003-a11y/Gemini_rag_chatbot.git
```

---

# Backend Setup

```bash
cd backend
```

Create virtual environment:

```bash
python -m venv venv
```

Activate environment:

### Windows
```bash
venv\\Scripts\\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create `.env` file:

```env
GOOGLE_API_KEY=your_api_key
```

Run backend:

```bash
uvicorn main:app --reload
```

---

# Frontend Setup

```bash
cd frontend
npm install
npm start
```

---

## Usage

1. Enter a website URL
2. Click ingest
3. Ask questions related to website content
4. Chatbot retrieves relevant context and generates answers

---

## Solution Approach

The chatbot follows a Retrieval-Augmented Generation (RAG) architecture.

### Workflow

1. Website content is ingested
2. Text is split into chunks
3. Embeddings are generated using Sentence Transformers
4. Embeddings are stored in FAISS vector database
5. User query is converted into embedding
6. Relevant chunks are retrieved
7. Gemini generates contextual response using retrieved information

---

## Deployment

### Frontend
Deployed on Vercel

### Backend
Deployed on Render

---

## Live Demo

https://gemini-rag-chatbot-czpg.vercel.app/

---

## Future Improvements

- PDF upload support
- Chat history
- Authentication
- Multi-document ingestion
- Improved UI/UX

---

## Author

Sreya
