from sqlalchemy import create_engine, Column, Integer, Text
from sqlalchemy.orm import declarative_base, sessionmaker
from pgvector.sqlalchemy import Vector
import numpy as np

# Define the SQLAlchemy model
Base = declarative_base()

class Test(Base):
    __tablename__ = 'test'
    id = Column(Integer, primary_key=True)
    content = Column(Text)
    embedding = Column(Vector(384))

# Set up the database connection
host = "localhost"
port = "5432"
user = "postgres"
password = "Akshay117"
dbname = "postgres"

connection_string = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{dbname}"
engine = create_engine(connection_string)

# Register the vector type with the connection
from pgvector.psycopg2 import register_vector
register_vector(engine.raw_connection())

# Create a session
Session = sessionmaker(bind=engine)
session = Session()

# Function to generate a sample embedding (replace this with your actual embedding generation)
def generate_embedding():
    return np.random.rand(384).tolist()

# Insert a sample record
def insert_record(content):
    embedding = generate_embedding()
    new_record = Test(content=content, embedding=embedding)
    session.add(new_record)
    session.commit()
    print(f"Inserted record with content: {content}")

# Main execution
if __name__ == "__main__":
    # Insert a few sample records
    insert_record("This is a test sentence.")
    insert_record("Another example for embedding.")
    insert_record("Vector embeddings are cool!")

    # Query to verify insertion
    results = session.query(Test).limit(3).all()
    for result in results:
        print(f"ID: {result.id}, Content: {result.content}, Embedding: {result.embedding[:5]}...")

    # Close the session
    session.close()