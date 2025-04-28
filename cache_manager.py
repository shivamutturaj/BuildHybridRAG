import pickle
import os

def save_embeddings(docs, embeddings, cache_path="embedding_cache.pkl"):
    with open(cache_path, "wb") as f:
        pickle.dump({"docs": docs, "embeddings": embeddings}, f)

def load_embeddings(cache_path="embedding_cache.pkl"):
    if not os.path.exists(cache_path):
        return None, None
    with open(cache_path, "rb") as f:
        data = pickle.load(f)
    return data["docs"], data["embeddings"]
