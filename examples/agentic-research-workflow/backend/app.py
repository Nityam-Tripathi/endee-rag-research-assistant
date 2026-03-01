from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pypdf import PdfReader
import uuid

from embeddings import get_embedding
from endee_client import ensure_index, insert_vector, search_vectors
from llm_agent import generate_answer

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory text store (Vector ID -> Chunk text)
TEXT_STORE = {}


class QueryRequest(BaseModel):
    question: str


# Ensure index exists at startup
@app.on_event("startup")
def startup_event():
    ensure_index()


# -------------------------
# DOCUMENT UPLOAD
# -------------------------

@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):

    try:
        reader = PdfReader(file.file)
        full_text = ""

        for page in reader.pages:
            text = page.extract_text()
            if text:
                full_text += text + "\n"

        if not full_text.strip():
            return {"error": "No extractable text found in PDF."}

        # Chunking
        chunk_size = 800
        overlap = 200

        chunks = []
        start = 0
        while start < len(full_text):
            end = start + chunk_size
            chunks.append(full_text[start:end])
            start += chunk_size - overlap

        inserted = 0

        for chunk in chunks:
            embedding = get_embedding(chunk)
            vector_id = str(uuid.uuid4())

            success = insert_vector(embedding, vector_id)

            if success:
                TEXT_STORE[vector_id] = chunk
                inserted += 1

        return {
            "message": f"{inserted} chunks indexed successfully"
        }

    except Exception as e:
        return {"error": str(e)}


# -------------------------
# ASK QUESTION
# -------------------------

@app.post("/ask")
def ask_question(request: QueryRequest):

    query_embedding = get_embedding(request.question)

    results = search_vectors(query_embedding, top_k=3)

    print("Search Results:", results)

    context_chunks = []

    for result in results:
        vector_id = result["id"]

        if vector_id in TEXT_STORE:
            context_chunks.append(TEXT_STORE[vector_id])

    if not context_chunks:
        return {
            "answer": "No relevant context found in uploaded documents.",
            "sources": []
        }

    context = "\n\n".join(context_chunks)

    answer = generate_answer(request.question, context)

    return {
        "answer": answer,
        "sources": context_chunks
    }