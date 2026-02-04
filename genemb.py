from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker
from pgvector.sqlalchemy import Vector
from sentence_transformers import SentenceTransformer

# Define the SQLAlchemy model
Base = declarative_base()

class Test(Base):
    __tablename__ = 'test'
    id = Column(Integer, primary_key=True)
    content = Column(String)
    embedding = Column(Vector(384))  # Adjust dimension as needed

# Set up the database connection
host = "localhost"
port = "5432"
user = "postgres"
password = "Akshay117"
dbname = "postgres"

connection_string = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{dbname}"

engine = create_engine(connection_string)

Session = sessionmaker(bind=engine)

# Load the embedding model
model = SentenceTransformer('BAAI/bge-small-en-v1.5')

def generate_embedding(text):
    """Generate an embedding for the given text using BAAI/bge-small-en-v1.5 model."""
    return model.encode(text, normalize_embeddings=True).tolist()

def insert_content(content):
    """Insert new content and its embedding into the test table."""
    session = Session()
    try:
        # Generate the embedding for the content
        embedding = generate_embedding(content)
        
        # Create a new Test object
        new_entry = Test(content=content, embedding=embedding)
        
        # Add and commit the new entry to the database
        session.add(new_entry)
        session.commit()
        print(f"Inserted content with ID: {new_entry.id}")
    except Exception as e:
        session.rollback()
        print(f"An error occurred: {e}")
    finally:
        session.close()

def main():
    # Accept new content from the user
    new_content = input("Enter new content to insert: ")
    
    # Insert the new content into the database
    insert_content(new_content)

if __name__ == "__main__":
    main()