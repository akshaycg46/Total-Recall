import psycopg2
from pgvector.psycopg2 import register_vector
from sentence_transformers import SentenceTransformer

# Load the model
model = SentenceTransformer('bge-small-en-v1.5')

# Text to embed
text = "Hello world! This is a sample text."

# Generate embedding
embedding = model.encode(text, normalize_embeddings=True)

# Print the embedding
print(f"Embedding shape: {embedding.shape}")
print(f"Embedding: {embedding}")

vector_str = str(embedding).replace(' ', '')

# Connect to your PostgreSQL database
conn = psycopg2.connect(
    host="localhost",
    database="postgres",
    user="postgres",
    password="Akshay117",
    port='5432'
)

# Create a cursor
cur = conn.cursor()

# Register the vector type
register_vector(conn)

# Insert embeddings into the database
for text, embedding in zip(text, embedding):
    cur.execute(
        "INSERT INTO test (content, embedding) VALUES (%s, %s)",
        (text, vector_str)
    )

conn.commit()