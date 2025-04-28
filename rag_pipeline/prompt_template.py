from langchain.prompts import PromptTemplate

def generate_prompt_template(model_choice="huggingface"):
    if model_choice == "huggingface":
        template = """Answer the question using the context below:\n{context}\nQuestion: {question}\nAnswer:"""
    else:
        template = """You are a helpful assistant. Use the information provided to answer accurately.\n\nContext:\n{context}\n\nQuestion: {question}\nAnswer:"""
    return PromptTemplate(input_variables=["context", "question"], template=template)
