'''
When you load documents, you must attach metadata — such as:
    -Document title
    -Source URL (for Confluence pages / GitHub files)

This metadata travels with the document through:
    -embedding ➔ storage ➔ retrieval ➔ final answer
    -so that when generating the answer, you can hyperlink back to the real source.
'''


import os

import os

def extract_data_from_sources(confluence_url: str, git_repo_path: str):
    documents = []
    
    # Mock Confluence data with real URL
    documents.append({
        "content": f"Content from Confluence page: {confluence_url}",
        "source": confluence_url
    })

    # Read Git files with path as source
    for file in os.listdir(git_repo_path):
        if file.endswith(".md") or file.endswith(".txt"):
            filepath = os.path.join(git_repo_path, file)
            with open(filepath, "r") as f:
                documents.append({
                    "content": f.read(),
                    "source": f"file://{filepath}"  # Local file link or GitHub raw link
                })
    
    return documents
