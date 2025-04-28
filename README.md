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
