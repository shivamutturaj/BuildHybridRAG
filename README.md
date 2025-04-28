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

-------------------------------------------------------------------------------------
CAG : 
Cache Embeddings to Disk (Avoid Recomputing)
✅ Problem:
-Embedding millions of docs is slow.
-You don't want to recompute every restart!

✅ Solution:
Save embeddings + metadata locally (e.g., .pkl or .parquet files).
------------------------------------------------------------------------------------
Hybrid Search (Semantic + Keyword)
✅ Problem:
Semantic search alone can miss important keywords.
E.g., you ask: "Python GIL issues" — semantic match is OK, but "GIL" keyword is critical.

✅ Solution:
Combine semantic similarity + keyword search.

-------------------------------------------------------------------------------------------
Expose as a FastAPI Server (RAG API Service)
✅ Problem:
Streamlit is nice for UI but not for backend serving.
We need a real API to plug into apps, bots, workflows.

✅ Solution:
Build a lightweight FastAPI app.

-------------------------------------------------------------------------------------------
Run api :
uvicorn app.rag_api:app --reload --host 0.0.0.0 --port 8000
-------------------------------------------------------------------------------------------
Example cURL Call:
curl -X POST "http://localhost:8000/ask" -H "Content-Type: application/json" -d '{"query":"What is the Python GIL?"}'
---------------------------------------------------------------------------------------------

[Confluence] + [GitHub] + [Local]
        ↓
 [Document Chunking + Cleaning]
        ↓
   [Embedding Cache Layer]
        ↓
 [ChromaDB / FAISS Vector DB]
        ↓
     [Hybrid Retriever]
        ↓
       [Prompt Templates]
        ↓
       [LLM Model]
        ↓
  [FastAPI Server for RAG API]

---------------------------------------------------------------------------------------------

our Complete RAG-as-a-Service has:

Data loaders (Confluence, GitHub, Local)	✅
Chunking long docs	✅
Embedding caching	✅
Hybrid retrieval (semantic + keyword)	✅
Hyperlinking sources	✅
Re-ranking documents	✅
Modular design (easy swap LLMs, DBs)	✅
Streamlit frontend (optional)	✅
FastAPI backend server (RAG API)	✅

--------------------------------------------------------------------------------------------------

Dockerize Everything (FastAPI + Vector DB)