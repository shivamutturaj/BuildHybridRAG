# BuildHybridRAG
Hybrid RAG

rag_project/
├── app.py                  # (your Streamlit app entry point)
├── rag_pipeline/
│   ├── __init__.py
│   ├── data_loader.py       # (for Confluence/Git data extraction)
│   ├── embedding.py         # (embedding model)
│   ├── vector_store.py      # (vector DBs: ChromaDB/FAISS)
│   ├── llm_loader.py        # (open-source and OpenAI models)
│   ├── retrieval.py         # (retriever logic)
│   ├── prompt_template.py   # (dynamic prompt generator)
│   ├── generator.py         # (generate final answer)
├── requirements.txt
├── README.md                # (optional: explain usage)
└── config.py                # (optional: configs for models, db, etc.)

-----------------------------------------------------------------------------------
Data loader:
 -Crawl full Confluence spaces | ✅
 -Crawl full GitHub repos | ✅
 -Local folder support | ✅
 -Full-source hyperlinks in answers | ✅
 -Clean text parsing | ✅

-----------------------------------------------------------------------------------
Problem:
Some Confluence pages or GitHub READMEs are very long (5K-10K tokens).
LLMs (like Mistral, LLaMA) have limited context windows (4K–32K tokens).

👉 So we chunk long docs into smaller, manageable pieces!

-----------------------------------------------------------------------------------

Problem:
Even after retrieval, not all top_k results are perfectly relevant.

Solution:
 -After getting top 10 candidates, re-rank them by:
 -Cosine similarity
 -Embedding closeness to query

-----------------------------------------------------------------------------------

Extract Confluence + GitHub + Local
    ↓
Chunk large documents
    ↓
Embed (SentenceTransformer or HF)
    ↓
Store in ChromaDB / FAISS
    ↓
Retrieve (Top 10)
    ↓
Re-rank (Top 3 most similar)
    ↓
Prompt (LLM)
    ↓
Answer with Hyperlinks
--------------------------------------------------------------------------------------
🎯 Your RAG stack is now:

Feature	Status
Chunking large files	✅
Embedding optimized chunks	✅
Semantic re-ranking retrieval	✅
Metadata-based filtering	✅
Streamlit UI	✅
Source hyperlinks in answers	✅