import psycopg2

from pgvector.db.config import db_config


def create_db_connection():
    params = db_config()
    # print(params)
    try:
        conn = psycopg2.connect(**params)
        ss = conn.cursor()
        ss.execute('CREATE EXTENSION IF NOT EXISTS vector;')

        ss.execute('''CREATE TABLE IF NOT EXISTS embeddings (
                  id SERIAL PRIMARY KEY,
                  embedding vector,
                  text text,
                  created_at timestamptz DEFAULT now()
                );''')
        embedding = [44.323223,244.4342,30.34]
        text = 'Hi'
        ss.execute("INSERT INTO embeddings (embedding, text) VALUES (%s, %s)",
                (embedding, text)
            )
#
#         # for i in db:
#         print(db)
        return conn
    except (Exception, psycopg2.Error) as error:
        print("Error while connecting", error)
    return None


create_db_connection()
