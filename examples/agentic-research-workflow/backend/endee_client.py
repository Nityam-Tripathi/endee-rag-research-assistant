import requests
import msgpack
import uuid

BASE_URL = "http://localhost:8080/api/v1"
INDEX_NAME = "research_index"


def ensure_index():
    try:
        response = requests.get(f"{BASE_URL}/index/list")
        data = response.json()

        indexes = [idx["name"] for idx in data.get("indexes", [])]

        if INDEX_NAME not in indexes:
            print("Creating index...")
            create_response = requests.post(
                f"{BASE_URL}/index/create",
                json={
                    "index_name": INDEX_NAME,
                    "dim": 384,
                    "space_type": "cosine"
                }
            )
            print("Create index status:", create_response.status_code)
    except Exception as e:
        print("Index check failed:", e)


def insert_vector(vector, vector_id):
    response = requests.post(
        f"{BASE_URL}/index/{INDEX_NAME}/vector/insert",
        headers={"Content-Type": "application/json"},
        json={
            "id": vector_id,
            "vector": vector
        }
    )

    return response.status_code == 200


def search_vectors(query_embedding, top_k=3):
    response = requests.post(
        f"{BASE_URL}/index/{INDEX_NAME}/search",
        json={
            "vector": query_embedding,
            "k": top_k
        }
    )

    if response.status_code != 200:
        print("Search error:", response.text)
        return []

    raw_results = msgpack.unpackb(response.content, raw=False)

    results = []
    for item in raw_results:
        score = item[0]
        vector_id = item[1]

        results.append({
            "score": score,
            "id": vector_id
        })

    return results