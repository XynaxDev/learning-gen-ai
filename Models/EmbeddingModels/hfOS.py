from langchain_huggingface import HuggingFaceEmbeddings
from dotenv import load_dotenv

load_dotenv()

# 1. Initialize the Embedding Model
embedding = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')

# 2. Define your Documents
documents = [
    "Delhi is the capital of India",
    "Kolkata is the capital of West Bengal",
    "Paris is the capital of France"
]

# 3. Generate the Vectors
vectors = embedding.embed_documents(documents)

# 4. Display Results
print(f"Number of documents embedded: {len(vectors)}")
print(f"Dimension of each vector: {len(vectors[0])}")