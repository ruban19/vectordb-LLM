from fastapi import FastAPI, Body
from typing import Dict, List
from pgvector.app.data_models.models import SearchRequest , upsert_model ,delete_model
from pgvector.db.connect import create_db_connection
import os
from langchain.embeddings import HuggingFaceHubEmbeddings


# creating instance of api and database modules
app = FastAPI()
connection = create_db_connection()
cursor = connection.cursor()
hg_embedding = HuggingFaceHubEmbeddings(
        huggingfacehub_api_token=os.getenv("HUGGINGFACEHUB_API_TOKEN")
    )


@app.get("/")
def read_root() -> Dict:
    return {"Hello": "Welcome to Vector Database API"}


@app.get('/search')
async def search_vector(input_data: SearchRequest):
    # Extract query from input
    embeddings_list = hg_embedding.embed_documents(input_data)
    result = []
    cursor.execute(f"""
                SELECT text,  1 - (embedding <=> '{embeddings_list[0]}') AS cosine_similarity
                FROM embeddings
                ORDER BY cosine_similarity desc
                LIMIT 1
            """)
    data = cursor.fetchall()
    for i in data:
        result.append(i)
    return {"message": result}


@app.get('/list_data')
async def show_data():
    result = []
    cursor.execute("""SELECT id,embedding,text,created_at  FROM embeddings;""")
    data = cursor.fetchall()
    for i in data:
        result.append(i)
    return {"message": result}


@app.put('/upsert_vector')
async def upsert_vector(data: upsert_model):
    # Extract identifier and updated vector from the request
    id = data.id
    embedding = data.embedding
    text = data.text
    created_at = data.created_at
    # Perform upsert in the vector database using pgvector
    cursor.execute(f"""
                    INSERT INTO embeddings (id,embedding, text, created_at)
                    VALUES (%s,%s,%s,%s)
                    ON CONFLICT ("id")
                    DO UPDATE SET embedding = excluded.embedding, text = excluded.text , created_at = excluded.created_at ;
                   """, (id,embedding,text,created_at))
    return {"message": "Vector updated successfully"}


@app.delete('/delete')
async def delete_vector(data: delete_model):
    # Extract identifier from the request
    id = data.id
    cursor.execute("DELETE FROM embeddings WHERE id = %s", (id,))
    return {"message": "Vector deleted successfully"}

