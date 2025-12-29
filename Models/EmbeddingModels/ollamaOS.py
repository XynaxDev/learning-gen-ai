from langchain_ollama import OllamaEmbeddings
from dotenv import load_dotenv

load_dotenv()

# 1. Initialize the Embedding Model
# nomic-embed-text is a high-performance, open-source local model
# make sure you have the model downloaded and Ollama running locally
embeddings = OllamaEmbeddings(model="nomic-embed-text")

# 2. Define your Query
query_text = "LangChain simplifies AI development"

# 3. Generate the Vector
# This turns your text into a list of 768 numbers locally
vector = embeddings.embed_query(query_text)

# 4. Display Results
print(f"User Query: {query_text}")
print(f"Vector Dimension: {len(vector)}")