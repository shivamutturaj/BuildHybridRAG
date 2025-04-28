from langchain.llms import HuggingFacePipeline, OpenAI

def get_llm(model_choice="huggingface", model_path=None):
    if model_choice == "huggingface":
        llm = HuggingFacePipeline.from_model_id(model_id=model_path, task="text-generation")
    elif model_choice == "openai":
        llm = OpenAI()
    else:
        raise ValueError("Unsupported LLM choice.")
    return llm
