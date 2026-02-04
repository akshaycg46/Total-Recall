from sqlalchemy import create_engine
from pgvector.sqlalchemy import Vector
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

# Build the connection string
host = "localhost"
port = "5432"
user = "postgres"
password = "Akshay117"
dbname = "postgres"

# Create the connection string
connection_string = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{dbname}"

# Create the SQLAlchemy engine
engine = create_engine(connection_string)

# Register the vector type with the connection

register_vector(engine.raw_connection())


# Assuming you have a model defined
class YourModel(Base):
    __tablename__ = 'test'
    id = Column(Integer, primary_key=True)
    vector_column = Column(Vector(3))  # 3 is the dimension of your vector

# Insert embeddings into the database
for text, embedding in zip(text, embedding):
    cur.execute(
        "INSERT INTO test (content, embedding) VALUES (%s, %s)",
        (text, vector_str)
    )

conn.commit()