from openai import OpenAI
import os
from backend.logger import get_logger

logger = get_logger("embeddings")


os.environ["OPENAI_API_KEY"] = "YOUR_OPENAI_KEY"  # or use .env

client = OpenAI()

def get_embedding(text):
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )
    return response.data[0].embedding

def cosine_similarity(vec1, vec2):
    import numpy as np
    a = np.array(vec1)
    b = np.array(vec2)
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))
