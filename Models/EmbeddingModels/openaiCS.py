from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv

load_dotenv()

# 1. Initialize the Embedding Model
embedding = OpenAIEmbeddings(model='text-embedding-3-large', dimensions=32)

# 2. Define your Query
query_text = "Delhi is the capital of India"

# 3. Generate the Vector
result = embedding.embed_query(query_text)

# 4. Display Results
print(f"User Query: {query_text}")
print(f"Vector Result (32 dims): {result}")