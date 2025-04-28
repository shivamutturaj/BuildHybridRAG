from rag_pipeline.data_loader import extract_data_from_sources
from rag_pipeline.embedding import get_embedding_model
from rag_pipeline.vector_store import setup_vector_db
from rag_pipeline.llm_loader import get_llm
from rag_pipeline.retrieval import retrieve_relevant_docs
from rag_pipeline.prompt_template import generate_prompt_template
from rag_pipeline.generator import generate_answer
import streamlit as st

def main():
    documents = extract_data_from_sources("https://dummy_confluence", "./git_repo")
    embed_model = get_embedding_model()
    db = setup_vector_db(documents, embed_model, db_type="chromadb")
    llm = get_llm(model_choice="huggingface", model_path="gpt2")
    prompt_template = generate_prompt_template(model_choice="huggingface")
    
    st.title("📚 RAG - Question Answering Bot")
    query = st.text_input("Ask a question:")

    if query:
        retrieved_docs = retrieve_relevant_docs(query, embed_model, db, db_type="chromadb")
        answer = generate_answer(query, retrieved_docs, llm, prompt_template)
        st.markdown(answer)

if __name__ == "__main__":
    main()
