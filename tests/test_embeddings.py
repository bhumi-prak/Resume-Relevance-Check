from models.embeddings_model import get_embedding, cosine_similarity

def test_embedding_vector():
    text = "Python SQL Machine Learning"
    vec = get_embedding(text)
    assert isinstance(vec, list), "Embedding should be a list"
    assert len(vec) > 0, "Embedding vector is empty"

def test_cosine_similarity():
    vec1 = get_embedding("Python SQL")
    vec2 = get_embedding("Python SQL Machine Learning")
    sim = cosine_similarity(vec1, vec2)
    assert 0 <= sim <= 1, "Cosine similarity should be between 0 and 1"
