from dotenv import load_dotenv
from dotenv import find_dotenv
load_dotenv(find_dotenv(usecwd=True))
from functions import read_rtf, create_collection, add_to_collection, query_collection
from os import getenv

if __name__ == "__main__":
    collection = create_collection()
    plain_text = read_rtf(getenv("FILENAME"))
    add_to_collection(plain_text,collection)
    while True:      
        query = input("Ask your question, type \"exit\" to leave:\n")
        if query == "exit":
            break
        print("Answer:",query_collection(collection,query))
    print("Goodbye")
    