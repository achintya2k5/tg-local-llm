import sqlite3
from typing import Any
import pandas as pd
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

def build_vector_store():
    connection=sqlite3.connect("messages_tele.db")

    tables=pd.read_sql_query("SELECT name FROM sqlite_master WHERE type='table';", connection)
    table_names=tables['name'].tolist()

    conversation_chunks=[]
    metadata=[]
    for table in table_names:
        try:
            df=pd.read_sql_query(f"SELECT * FROM {table};", connection)

            if 'message_id' in df.columns:
                if 'timestamp' in df.columns:
                    df=df.sort_values(by='timestamp')

                if 'text' in df.columns:
                    messages=df['text'].dropna().tolist()
                    messages = [msg for msg in messages if isinstance(msg, str)]
                else:
                    messages=[]

                chunk_size=10
                for i in range(0, len(messages), chunk_size):
                    chunk="\n".join(messages[i:i+chunk_size])
                    conversation_chunks.append(chunk)
                    metadata.append({
                        "table":table,
                        "start_index":i,
                        "end_index":i+chunk_size
                    })
        except Exception as e:
            print(f"Skipping table {table} due to error: {e}")

    connection.close()

    if not conversation_chunks:
        raise ValueError("No conversation messages found to build vector store.")

    model=SentenceTransformer("all-mpnet-base-v2")
    embeddings=model.encode(conversation_chunks,show_progress_bar=True)
    embeddings_array=np.asarray(embeddings, dtype="float32")

    dimension=embeddings_array.shape[1]
    index: Any=faiss.IndexFlatL2(dimension)
    index.add(embeddings_array)
    return model, index, conversation_chunks, metadata
