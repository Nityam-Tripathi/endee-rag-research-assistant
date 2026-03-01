from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def generate_answer(question: str, context: str):

    prompt = f"""
You are an intelligent research assistant.

Use ONLY the provided context to answer the question.
If the context is insufficient, clearly say so.

Question:
{question}

Context:
{context}

Answer:
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
    )

    return response.choices[0].message.content