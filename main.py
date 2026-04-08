from api_telegram.telegram_listener import run_api
from vec_dbs.vec_db import build_vector_store
from vec_dbs.query import query_vector_store
from llm.mistral_runner import llm_gen

if __name__=="__main__":
    run_api()
    model,index,chunks,metadata=build_vector_store()
    query=input("Enter your query: ")
    results=query_vector_store(query, model, index, chunks)
    retrieved_chunks=[text for text, _ in results]
    llm_gen(retrieved_chunks, query)