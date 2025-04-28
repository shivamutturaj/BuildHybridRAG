
'''
to pull both content and true source
'''

def retrieve_relevant_docs(query, embed_model, db, db_type="chromadb", top_k=5):
    query_emb = embed_model.encode([query])

    if db_type == "chromadb":
        results = db.query(query_embeddings=query_emb.tolist(), n_results=top_k)
        return [(doc, meta["source"]) for doc, meta in zip(results['documents'][0], results['metadatas'][0])]
    
    elif db_type == "faiss":
        index, contents, sources = db
        D, I = index.search(query_emb, top_k)
        return [(contents[i], sources[i]) for i in I[0]]

