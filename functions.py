import chromadb
from chromadb.utils import embedding_functions
from openai import OpenAI
from striprtf.striprtf import rtf_to_text # type: ignore
from os import getenv

def create_collection():
    chroma_client = chromadb.PersistentClient(path="./chroma_db")
    try:
        chroma_client.delete_collection("Curriculumvitae")
    except:
        pass
    openai_ef = embedding_functions.OpenAIEmbeddingFunction(
    api_key=getenv("OPENAI_API_KEY"),
    model_name="text-embedding-3-small"
    )
    collection = chroma_client.get_or_create_collection(
    name="Curriculumvitae",
    embedding_function=openai_ef
    )
    return collection



def read_rtf(file):
    with open(file, "r", encoding="utf-8", errors="ignore") as f:
        rtf_content = f.read()
    return rtf_to_text(rtf_content)

def chunk_text(text, chunk_size=500, overlap=50):
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start += chunk_size - overlap
    return chunks

def add_to_collection(text,collection):
    all_chunks = []
    ids = []
    chunks = chunk_text(text)
    for j, chunk in enumerate(chunks):
        all_chunks.append(chunk)
        ids.append(f"doc_chunk{j}")
    collection.add(
        documents=all_chunks,
        ids=ids
    )

def query_collection(collection, query):
    results = collection.query(
        query_texts=[query],
        n_results=3
    )

    context = "\n".join(results["documents"][0])
    print("Retrieved context:\n", context)

    client_oa = OpenAI(api_key=getenv("OPENAI_API_KEY"),)

    prompt = f"Answer the question based on the context:\n\n{context}\n\nQuestion: {query}"

    response = client_oa.chat.completions.create(
        model="gpt-4.1",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content
