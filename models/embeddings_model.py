from openai import OpenAI
import os
import numpy as np

os.environ["OPENAI_API_KEY"] = "YOUR_OPENAI_KEY"

client = OpenAI()

def get_embedding(text):
    """Returns embedding vector for given text"""
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )
    return response.data[0].embedding

def cosine_similarity(vec1, vec2):
    a = np.array(vec1)
    b = np.array(vec2)
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))
