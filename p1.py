from sqlalchemy import create_engine, text
from pgvector.sqlalchemy import Vector
from sentence_transformers import SentenceTransformer
import openai

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, Session
from pgvector.sqlalchemy import Vector


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

session = Session(engine)

# Initialize SentenceTransformer model
model = SentenceTransformer('BAAI/bge-small-en-v1.5')

# OpenAI API setup (replace with your API key)
openai.api_key = "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"

def generate_embedding(text):
    return model.encode(text, normalize_embeddings=True).tolist()

# Perform similarity search
def similarity_search(query_vector, limit=5):
    return session.query(Test).order_by(
        Test.embedding.l2_distance(query_vector)
    ).limit(limit).all()

def generate_response(prompt, context):
    system_message = "You are a helpful assistant. Use the provided context to answer the question."
    messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": f"Context: {context}\n\nQuestion: {prompt}"}
    ]
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        max_tokens=150
    )
    return response.choices[0].message['content'].strip()

def process_prompt(prompt):
    # Generate embedding for the prompt
    prompt_embedding = generate_embedding(prompt)

    # Perform similarity search
    similar_texts = similarity_search(prompt_embedding)
    print(" ----------> " , similar_texts)
    for doc in similar_texts:  # Iterate over the list of Document objects
        # If you need to calculate similarity, do it separately
        #similarity = 1 - doc.embedding.l2_distance(prompt_embedding)
        print(f"ID: {doc.id}, Content: {doc.content}")

    # Prepare context from similar texts
    context = "\n".join([text for text, _ in similar_texts])

    # Generate response using LLM
    response = generate_response(prompt, context)

    return response

# Example usage
prompt = "Where did I keep my keys?"
response = process_prompt(prompt)
print(f"Prompt: {prompt}")
print(f"Response: {response}")