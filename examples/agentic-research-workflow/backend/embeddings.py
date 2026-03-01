from sentence_transformers import SentenceTransformer

# Load once globally
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

def get_embedding(text: str):
    return model.encode(text).tolist()