from dotenv import load_dotenv
from dotenv import find_dotenv
load_dotenv(find_dotenv(usecwd=True))
from functions import read_rtf, chunk_text, create_collection
from openai import OpenAI
from os import getenv

if __name__ == "__main__":
    collection = create_collection()
    plain_text = read_rtf("CV_Konrad_Kowalczyk_DataArchitect-_English_2025_08.rtf")
    all_chunks = []
    ids = []

    chunks = chunk_text(plain_text)
    for j, chunk in enumerate(chunks):
        all_chunks.append(chunk)
        ids.append(f"doc_chunk{j}")

    collection.add(
        documents=all_chunks,
        ids=ids
    )

    query = "What does the document say about retrieval?"
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

    print("Answer:", response.choices[0].message.content)
