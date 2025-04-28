'''
 to insert real hyperlinks
'''
def generate_answer(query, retrieved_docs, llm, prompt_template):
    context = "\n".join([doc for doc, _ in retrieved_docs])
    sources = [source for _, source in retrieved_docs]
    prompt = prompt_template.format(context=context, question=query)
    answer = llm(prompt)

    # Create clickable links
    hyperlinks = "\n".join([f"[Source {i+1}]({source})" for i, source in enumerate(sources)])
    return answer + "\n\n### Sources:\n" + hyperlinks

