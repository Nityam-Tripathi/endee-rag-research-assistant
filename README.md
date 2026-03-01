AI Research Assistant using RAG + Endee Vector Database
📌 Overview 
This project is a Retrieval-Augmented Generation (RAG) Research Assistant built using:
⚡ Endee (High-performance vector database)
🧠 Sentence Transformers (all-MiniLM-L6-v2)
🤖 Groq LLM (LLaMA 3.1 8B Instant)
🚀 FastAPI backend
📄 PDF ingestion + intelligent chunking
🎯 Clean vector + Python text-store architecture

The system allows users to:
1. Upload PDF research documents
2. Automatically chunk and embed them
3. Store embeddings in Endee
4. Ask natural language questions
5. Get context-grounded answers from an LLM

🧠 System Architecture
          User
           ↓
      Upload PDF
           ↓
    Text Extraction
           ↓
Chunking (800 tokens + overlap)
           ↓
SentenceTransformer Embeddings
           ↓
      Endee Vector DB
           ↓
      User Question
           ↓
       Embedding
           ↓
Vector Search (Top-K)
           ↓
Retrieve Relevant Chunks
           ↓
      Groq LLM
           ↓
Final Context-Grounded Answer

🏗 Tech Stack
Layer	Technology
Backend API	FastAPI
Embedding Model	sentence-transformers/all-MiniLM-L6-v2
Vector Database	Endee (AVX2 optimized)
LLM	Groq – llama-3.1-8b-instant
File Parsing	pypdf
Deployment	Docker (Endee)

📂 Project Structure
backend/
│
├── app.py              # FastAPI application
├── embeddings.py       # Embedding model loader
├── endee_client.py     # Endee API wrapper
├── llm_agent.py        # LLM generation logic
├── requirements.txt


⚙️ Installation Guide
1️⃣ Start Endee Vector Database
docker compose up -d

Endee runs on:

http://localhost:8080
2️⃣ Install Python Dependencies
pip install -r requirements.txt
3️⃣ Set Environment Variable

Create .env file:

GROQ_API_KEY=your_api_key_here
4️⃣ Start Backend
uvicorn app:app --reload --port 8000

API available at:

http://localhost:8000/docs
📥 API Endpoints
Upload Document
POST /upload

Uploads a PDF → chunks → embeds → stores in Endee.

Ask Question
POST /ask

Request:

{
  "question": "What is the main contribution of this paper?"
}

Response:

{
  "answer": "...LLM generated answer...",
  "sources": ["chunk1", "chunk2"]
}
🔬 Technical Design Decisions
✅ Why Endee?

SIMD-optimized

High-performance C++ backend

MessagePack search responses

Lightweight and open-source

✅ Why Separate TEXT_STORE?

Endee stores vectors only.
We store raw text in Python memory to:

Maintain flexibility

Avoid metadata parsing overhead

Simplify retrieval pipeline

✅ Why 800 Chunk Size?

Balanced context window usage

Works well with MiniLM embeddings

Avoids LLM truncation

✅ Why RAG?

Prevents hallucinations by grounding answers in retrieved documents.

📊 Performance Characteristics

Embedding Dimension: 384

Index Space Type: Cosine similarity

Top-K Retrieval: 3

LLM Temperature: 0.3 (low hallucination)

🧪 Example Workflow

Upload research paper PDF

Ask:
"How does the proposed model improve accuracy?"

System retrieves top 3 relevant chunks

LLM generates context-aware answer

Sources returned

🔐 Limitations

TEXT_STORE is in-memory (not persistent)
Single-user system
No document deletion endpoint
No authentication layer
Not production-hardened

🚀 Future Improvements

Persistent metadata store (Redis / PostgreSQL)
Multi-document management
User authentication
Re-ranking layer
Hybrid sparse + dense search
Streaming LLM responses
Frontend UI
Agentic multi-step reasoning
