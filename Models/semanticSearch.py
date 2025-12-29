import numpy as np
from langchain_openai import OpenAIEmbeddings
from sklearn.metrics.pairwise import cosine_similarity
from dotenv import load_dotenv

load_dotenv()

# 1. Initialize the Embedding Model
# We'll use 256 dimensions to keep it fast and lean
embedding = OpenAIEmbeddings(model='text-embedding-3-large', dimensions=256)

# 2. Your Knowledge Base
documents = [
    "Virat Kohli is an Indian cricketer known for his aggressive batting and leadership.",
    "MS Dhoni is a former Indian captain famous for his calm demeanor and finishing skills.",
    "Sachin Tendulkar, also known as the 'God of Cricket', holds many batting records.",
    "Rohit Sharma is known for his elegant batting and record-breaking double centuries.",
    "Jasprit Bumrah is an Indian fast bowler known for his unorthodox action and yorkers."
]

# Pre-compute document embeddings (only do this once!)
print("Embedding knowledge base...")
doc_embeddings = embedding.embed_documents(documents)

# 3. Interactive Search Loop
print("\nCricket Search Tool Ready! (Type 'exit' to stop)")
while True:
    query = input("\nSearch for a player: ").strip()
    
    if query.lower() == 'exit':
        break

    # Generate embedding for the user's query
    query_embedding = embedding.embed_query(query)

    # 4. Calculate Similarity and Display Results
    # We compare the query vector against ALL doc vectors at once
    scores = cosine_similarity([query_embedding], doc_embeddings)[0]
    
    # Find the index of the highest score
    best_index = np.argmax(scores)
    best_score = scores[best_index]

    print(f"Result: {documents[best_index]}")
    print(f"Confidence: {best_score:.4f}")