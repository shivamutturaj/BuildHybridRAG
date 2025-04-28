'''
When you load documents, you must attach metadata — such as:
    -Document title
    -Source URL (for Confluence pages / GitHub files)

This metadata travels with the document through:
    -embedding ➔ storage ➔ retrieval ➔ final answer
    -so that when generating the answer, you can hyperlink back to the real source.

This function automatically:
    -Fetches up to 1000s of pages from a Space
    -Retrieves full page HTML content (or you can convert it to plain text easily)
    -Links every page to its real Confluence URL
'''

import requests
import os
from requests.auth import HTTPBasicAuth
from github import Github
from rag_pipeline.chunker import split_into_chunks

def extract_data_from_confluence(confluence_base_url, space_key, username, api_token):
    documents = []
    url = f"{confluence_base_url}/wiki/rest/api/content?spaceKey={space_key}&expand=body.storage&limit=100"

    auth = HTTPBasicAuth(username, api_token)
    headers = {"Accept": "application/json"}

    while url:
        response = requests.get(url, headers=headers, auth=auth)
        if response.status_code != 200:
            raise Exception(f"Failed to fetch Confluence data: {response.text}")

        data = response.json()
        for page in data.get("results", []):
            content = page["body"]["storage"]["value"]
            title = page["title"]
            page_url = f"{confluence_base_url}/wiki{page['_links']['webui']}"
            documents.append({
                "content": content,
                "source": page_url,
                "title": title
            })

        # Pagination
        if "_links" in data and "next" in data["_links"]:
            url = confluence_base_url + "/wiki" + data["_links"]["next"]
        else:
            url = None

    return documents

# from bs4 import BeautifulSoup

# def html_to_text(html_content):
#     soup = BeautifulSoup(html_content, "html.parser")
#     return soup.get_text(separator="\n")

def extract_data_from_github_repo(repo_url, github_token):
    documents = []
    
    repo_name = repo_url.replace("https://github.com/", "").strip("/")
    g = Github(github_token)
    repo = g.get_repo(repo_name)

    contents = repo.get_contents("")
    while contents:
        file_content = contents.pop(0)
        if file_content.type == "dir":
            contents.extend(repo.get_contents(file_content.path))
        else:
            if file_content.path.endswith((".md", ".txt", ".py")):  # Choose file types
                content = file_content.decoded_content.decode("utf-8")
                file_link = f"https://github.com/{repo_name}/blob/main/{file_content.path}"
                documents.append({
                    "content": content,
                    "source": file_link,
                    "title": file_content.path
                })

    return documents

'''
Each large doc becomes many small embeddings
Retrieval is faster + more accurate
No "overflow" errors on LLM context
'''

def extract_data_from_sources(confluence_args=None, github_args=None, local_folder=None):
    documents = []

    if confluence_args:
        confluence_docs = extract_data_from_confluence(**confluence_args)
        for doc in confluence_docs:
            chunks = split_into_chunks(doc["content"])
            for idx, chunk in enumerate(chunks):
                documents.append({
                    "content": chunk,
                    "source": doc["source"],
                    "title": f"{doc['title']} (chunk {idx})"
                })

    if github_args:
        github_docs = extract_data_from_github_repo(**github_args)
        for doc in github_docs:
            chunks = split_into_chunks(doc["content"])
            for idx, chunk in enumerate(chunks):
                documents.append({
                    "content": chunk,
                    "source": doc["source"],
                    "title": f"{doc['title']} (chunk {idx})"
                })

    if local_folder:
        for file in os.listdir(local_folder):
            if file.endswith(".md") or file.endswith(".txt"):
                with open(os.path.join(local_folder, file), "r") as f:
                    content = f.read()
                    chunks = split_into_chunks(content)
                    for idx, chunk in enumerate(chunks):
                        documents.append({
                            "content": chunk,
                            "source": f"file://{local_folder}/{file}",
                            "title": f"{file} (chunk {idx})"
                        })

    return documents
