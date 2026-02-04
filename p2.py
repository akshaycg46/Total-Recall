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

def total_recall(prompt):

    # Generate an embedding for the prompt
    prompt_embedding = generate_embedding(prompt)

    # Perform the similarity search
    closest_match = similarity_search(prompt_embedding)

    # Display the closest match
    if closest_match:
        print(f"Closest match ID: {closest_match.id}")
        print(f"Content: {closest_match.content}")
    else:
        print("No match found.")
    return closest_match.content     

def generate_embedding(text):
    return model.encode(text, normalize_embeddings=True).tolist()

def similarity_search(prompt_embedding):
    session = Session()
    try:
        # Perform the similarity search using cosine distance
        result = session.query(Test).order_by(
            Test.embedding.cosine_distance(prompt_embedding)
        ).first()  # Get the closest match
        return result
    finally:
        session.close()

def main():
    # Accept a prompt from the user
    prompt = input("Enter your prompt: ")

    # Generate an embedding for the prompt
    prompt_embedding = generate_embedding(prompt)

    # Perform the similarity search
    closest_match = similarity_search(prompt_embedding)

    # Display the closest match
    if closest_match:
        print(f"Closest match ID: {closest_match.id}")
        print(f"Content: {closest_match.content}")
    else:
        print("No match found.")

if __name__ == "__main__":
    main()