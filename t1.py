from openai import OpenAI
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
engine = create_engine('postgresql+psycopg2://user:password@host:port/database')
Session = sessionmaker(bind=engine)

# Load the embedding model
embedding_model = SentenceTransformer('BAAI/bge-small-en-v1.5')

# Initialize OpenAI API client
openai.api_key = "your_openai_api_key"

def generate_embedding(text):
    """Generate an embedding for the given text."""
    return embedding_model.encode(text, normalize_embeddings=True).tolist()

def similarity_search(prompt_embedding):
    session = Session()
    try:
        result = session.query(Test).order_by(
            Test.embedding.cosine_distance(prompt_embedding)
        ).first()  # Get the closest match
        return result.content if result else None
    finally:
        session.close()

def generate_response_with_llama(context):
    """Generate a response using the Llama model with the given context."""
    response = openai.Completion.create(
        model="llama-3-8b-instruct",
        prompt=f"Context: {context}\n\nGenerate a detailed response based on the above context.",
        max_tokens=150
    )
    return response.choices[0].text.strip()

def main():
    # Accept a prompt from the user
    prompt = input("Enter your query: ")

    # Generate an embedding for the prompt
    prompt_embedding = generate_embedding(prompt)

    # Perform the similarity search
    context = similarity_search(prompt_embedding)

    # Generate and display the response
    if context:
        response = generate_response_with_llama(context)
        print("Response:", response)
    else:
        print("No relevant content found.")

if __name__ == "__main__":
    main()