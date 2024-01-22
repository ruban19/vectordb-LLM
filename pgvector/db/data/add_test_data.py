from pgvector import BASE_DIR  # simply because we need to load .env
from pgvector.db.connect import create_db_connection

import os
import psycopg2
from langchain.embeddings.base import Embeddings
from langchain.embeddings import HuggingFaceHubEmbeddings


if __name__ == '__main__':
    print(os.getenv('EMBEDDING_MODEL'))
    # Write five example sentences that will be converted to embeddings
    texts = [
        "I like to eat broccoli and bananas.",
        "I ate a banana and spinach smoothie for breakfast.",
        "Chinchillas and kittens are cute.",
        "My sister adopted a kitten yesterday.",
        "Look at this cute hamster munching on a piece of broccoli.",
    ]
    print(texts)
    # openai.api_key = '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'
    embeddings = HuggingFaceHubEmbeddings(
        huggingfacehub_api_token=os.getenv("HUGGINGFACEHUB_API_TOKEN")
    )
    # embeddings = get_embeddings(texts, os.getenv('EMBEDDING_MODEL'))
    embeddings_list = embeddings.embed_documents(texts)
    print(embeddings_list)
    # Write text and embeddings to database
    connection = create_db_connection()
    cursor = connection.cursor()
    try:
        for text, embedding in zip(texts, embeddings):
            cursor.execute(
                "INSERT INTO embeddings (embedding, text) VALUES (%s, %s)",
                (embedding, text)
            )
        connection.commit()
    except (Exception, psycopg2.Error) as error:
        print("Error while writing to DB", error)
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()