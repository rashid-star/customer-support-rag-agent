# 🤖 Customer Support RAG Agent

> AI-powered Customer Support + Escalation System using  
> LangChain • FAISS • HuggingFace • Groq • FastAPI • Streamlit

---

# 🚀 Project Overview

This project is an intelligent customer support chatbot built using **RAG (Retrieval-Augmented Generation)** architecture.

The chatbot can:

✅ Answer customer support questions  
✅ Search internal knowledge base  
✅ Handle payment/shipping/account issues  
✅ Escalate sensitive queries to human support  
✅ Provide support contact details  
✅ Run through FastAPI backend + Streamlit frontend

---

# 🧠 How The System Works

```txt
User Question
      ↓
Frontend (Streamlit)
      ↓
FastAPI Backend
      ↓
Retriever (FAISS)
      ↓
Relevant Documents
      ↓
Groq LLM
      ↓
Escalation System
      ↓
Final AI Response
```

---

# 🏗️ Project Structure

```txt
customer_support_agent/
│
├── agent/
│   ├── chatbot.py
│   ├── retriever.py
│   └── escalation.py
│
├── api/
│   └── main.py
│
├── frontend/
│   └── app.py
│
├── ingestion/
│   └── ingest.py
│
├── faiss_index/
│
├── data/
│
├── .env
├── pyproject.toml
└── uv.lock
```

---

# ⚡ Features

## ✅ RAG Architecture

Uses Retrieval-Augmented Generation:

- retrieve relevant support knowledge
- generate grounded responses
- reduce hallucination

---

## ✅ Semantic Search

Uses:

- HuggingFace Embeddings
- FAISS Vector Database

for intelligent semantic similarity search.

---

## ✅ Escalation Workflow

Sensitive issues automatically escalate:

- payment issues
- refund problems
- account issues
- low-confidence responses

---

## ✅ FastAPI Backend

Provides:

- REST API
- validation
- structured responses
- Swagger docs

---

## ✅ Streamlit Frontend

Provides:

- chat interface
- message history
- escalation warnings
- frontend/backend communication

---

# 🧩 Tech Stack

| Technology  | Purpose            |
| ----------- | ------------------ |
| LangChain   | RAG Pipeline       |
| FAISS       | Vector Database    |
| HuggingFace | Embeddings         |
| Groq        | LLM                |
| FastAPI     | Backend API        |
| Streamlit   | Frontend           |
| Pandas      | Dataset Processing |

---

# 📚 Dataset

Dataset used:

```txt
Bitext Customer Support Dataset
```

Contains:

- customer queries
- support responses
- categories
- intents

---

# 🔄 Complete RAG Flow

## 1️⃣ Data Ingestion

`ingestion/ingest.py`

This script:

- loads dataset
- cleans text
- creates documents
- splits chunks
- generates embeddings
- stores vectors in FAISS

---

## 2️⃣ Embedding Generation

Text chunks are converted into vectors using:

```python
sentence-transformers/all-MiniLM-L6-v2
```

This helps the chatbot understand semantic meaning.

---

## 3️⃣ Vector Database

FAISS stores vector embeddings.

This allows:

- fast semantic search
- similarity matching
- context retrieval

---

## 4️⃣ Retrieval System

`agent/retriever.py`

When user asks question:

```txt
User Query
   ↓
Embedding Conversion
   ↓
FAISS Similarity Search
   ↓
Top Relevant Documents
```

Retriever returns:

- content
- metadata
- similarity scores

---

## 5️⃣ Chatbot Pipeline

`agent/chatbot.py`

Main responsibilities:

✅ detect customer intent  
✅ retrieve relevant knowledge  
✅ generate AI response  
✅ handle escalation logic  
✅ return structured response

---

# 🛑 Escalation System

`agent/escalation.py`

Handles:

- payment issues
- refund issues
- delivery issues
- account problems
- low-confidence responses

Example:

```txt
"money deducted but payment failed"
```

↓

```txt
Escalate to Payment Support Team
```

---

# 🌐 Backend API

`api/main.py`

FastAPI backend provides:

## Main Endpoint

```txt
POST /chat
```

## Health Check

```txt
GET /
```

---

# 📖 Swagger API Docs

After running backend:

```txt
http://127.0.0.1:8000/docs
```

---

# 💬 Frontend

`frontend/app.py`

Built using Streamlit.

Features:

- clean chat UI
- message history
- escalation warnings
- API integration

---

# ⚙️ Installation

## 1️⃣ Create Virtual Environment

```powershell
uv venv
```

Activate:

```powershell
.venv\Scripts\activate
```

---

## 2️⃣ Install Dependencies

```powershell
uv add pandas langchain langchain-community langchain-huggingface faiss-cpu fastapi uvicorn streamlit python-dotenv groq sentence-transformers
```

---

# 🔑 Environment Variables

Create `.env`

```env
GROQ_API_KEY=your_api_key_here
```

---

# 🧠 Create FAISS Vector Database

Run ingestion:

```powershell
python ingestion/ingest.py
```

This creates:

```txt
faiss_index/
```

---

# 🚀 Run Backend

```powershell
uvicorn api.main:app --reload
```

Backend URL:

```txt
http://127.0.0.1:8000
```

---

# 🎨 Run Frontend

```powershell
streamlit run frontend/app.py
```

Frontend URL:

```txt
http://localhost:8501
```

---

# 🧪 Example Queries

## Order Support

```txt
How can I cancel my order?
```

---

## Payment Issue

```txt
Payment failed but money deducted
```

---

## Delivery Issue

```txt
Where is my order?
```

---

## Account Issue

```txt
Forgot my password
```

---

# 📦 Example API Response

```json
{
  "answer": "Please contact payment support...",
  "escalate": true,
  "confidence": "high"
}
```

---

# 🔥 Current Improvements

✅ Better retrieval quality  
✅ Similarity scoring  
✅ Intent detection  
✅ Escalation workflow  
✅ Support routing  
✅ Professional backend structure  
✅ Interactive frontend UI

---

# 🚧 Future Improvements

- Conversation memory
- Admin dashboard
- Multi-language support
- WhatsApp integration
- CRM integration
- PostgreSQL logging
- Authentication
- Cloud deployment

---

# 🎯 Learning Outcomes

This project demonstrates:

- RAG Architecture
- Semantic Search
- Vector Databases
- Embeddings
- FastAPI Backend
- Streamlit Frontend
- LLM Integration
- Escalation Workflow
- AI System Design
- Backend Engineering

---

# 👨‍💻 Author

## Rashid Chaudhary

Customer Support + Escalation AI Agent Project
