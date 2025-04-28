from fastapi import FastAPI
from pydantic import BaseModel
from rag_pipeline.generator import generate_answer
from rag_pipeline.retrieval import hybrid_retrieve
from rag_pipeline.vector_store import load_vector_db
from rag_pipeline.embedding_model import load_embedding_model
from rag_pipeline.llm_model import load_llm_model

app = FastAPI()

# Load everything at startup
embed_model = load_embedding_model(model_name="all-MiniLM-L6-v2")
vector_db = load_vector_db(db_type="chromadb")
llm = load_llm_model(llm_choice="mistral")

class QueryRequest(BaseModel):
    query: str

@app.post("/ask")
def ask_query(request: QueryRequest):
    retrieved_docs = hybrid_retrieve(
        query=request.query,
        embed_model=embed_model,
        db=vector_db,
        db_type="chromadb",
        top_k=10,
        rerank_top_k=5
    )
    answer = generate_answer(request.query, retrieved_docs, llm, prompt_template="{context}\n\nQ: {question}\nA:")
    return {"answer": answer}
