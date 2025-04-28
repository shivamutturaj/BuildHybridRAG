
'''
to pull both content and true source
Pulls top 10 from Vector DB
Ranks top 3 by pure semantic match
Maximizes answer qualit
'''

import numpy as np

def cosine_similarity(vec1, vec2):
    return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))

def retrieve_relevant_docs(query, embed_model, db, db_type="chromadb", top_k=5, rerank_top_k=3):
    query_emb = embed_model.encode([query])

    if db_type == "chromadb":
        results = db.query(query_embeddings=query_emb.tolist(), n_results=top_k)
        docs_and_metas = list(zip(results['documents'][0], results['metadatas'][0]))
        doc_embeddings = embed_model.encode([doc for doc, _ in docs_and_metas])

    elif db_type == "faiss":
        index, contents, sources = db
        D, I = index.search(query_emb, top_k)
        docs_and_metas = [(contents[i], {"source": sources[i]}) for i in I[0]]
        doc_embeddings = embed_model.encode([doc for doc, _ in docs_and_metas])

    sims = [cosine_similarity(query_emb.flatten(), doc_emb.flatten()) for doc_emb in doc_embeddings]
    sorted_docs = sorted(zip(docs_and_metas, sims), key=lambda x: x[1], reverse=True)
    
    top_docs = sorted_docs[:rerank_top_k]
    return [(doc, meta["source"]) for (doc, meta), _ in top_docs]


def hybrid_retrieve(query, embed_model, db, db_type="chromadb", top_k=5, rerank_top_k=3):
    query_emb = embed_model.encode([query])
    query_keywords = query.lower().split()

    if db_type == "chromadb":
        results = db.query(query_embeddings=query_emb.tolist(), n_results=top_k)
        docs_and_metas = list(zip(results['documents'][0], results['metadatas'][0]))
        doc_embeddings = embed_model.encode([doc for doc, _ in docs_and_metas])

    elif db_type == "faiss":
        index, contents, sources = db
        D, I = index.search(query_emb, top_k)
        docs_and_metas = [(contents[i], {"source": sources[i]}) for i in I[0]]
        doc_embeddings = embed_model.encode([doc for doc, _ in docs_and_metas])

    sims = [cosine_similarity(query_emb.flatten(), doc_emb.flatten()) for doc_emb in doc_embeddings]

    # Boost score if query keywords found
    scores = []
    for (doc, meta), sim in zip(docs_and_metas, sims):
        text = doc.lower()
        keyword_hits = sum([kw in text for kw in query_keywords])
        boosted_score = sim + (0.01 * keyword_hits)  # small boost
        scores.append((doc, meta["source"], boosted_score))

    # Sort
    sorted_docs = sorted(scores, key=lambda x: x[2], reverse=True)
    top_docs = sorted_docs[:rerank_top_k]
    
    return [(doc, source) for doc, source, _ in top_docs]


