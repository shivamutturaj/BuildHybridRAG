import chromadb
from chromadb.config import Settings
import faiss

def setup_vector_db(documents, embed_model, db_type="chromadb"):
    contents = [doc["content"] for doc in documents]
    sources = [doc["source"] for doc in documents]

    embeddings = embed_model.encode(contents)

    if db_type == "chromadb":
        client = chromadb.Client(Settings())
        collection = client.create_collection(name="rag_collection")
        for idx, content in enumerate(contents):
            collection.add(
                documents=[content],
                embeddings=[embeddings[idx].tolist()],
                metadatas=[{"source": sources[idx]}],  # real source link
                ids=[str(idx)]
            )
        return collection

    elif db_type == "faiss":
        dim = embeddings.shape[1]
        index = faiss.IndexFlatL2(dim)
        index.add(embeddings)
        return index, contents, sources # returns content and source with index
