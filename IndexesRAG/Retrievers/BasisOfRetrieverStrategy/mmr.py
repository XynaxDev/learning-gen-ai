# MMR: Max Marginal Retriever

from langchain_community.vectorstores import FAISS # pip install faiss-cpu
from langchain_core.documents import Document
from langchain_ollama import OllamaEmbeddings

# 1. Your source Document
documents = [
    Document(
        page_content="Inception is a science fiction film by Christopher Nolan about a skilled thief who enters people's dreams to steal secrets. The story explores dreams within dreams, layered realities, and the difficulty of distinguishing between illusion and reality."
    ),
    Document(
        page_content="The Dark Knight is a superhero film directed by Christopher Nolan featuring Batman and the Joker. The movie is famous for Heath Ledger's performance and focuses on chaos, morality, and the psychological conflict between hero and villain."
    ),
    Document(
        page_content="Interstellar is a science fiction space film by Christopher Nolan about astronauts traveling through a wormhole to find a new home for humanity. The story explores black holes, time dilation, gravity, and emotional connections."
    ),
    Document(
        page_content="Dunkirk is a war film by Christopher Nolan about the evacuation of Allied soldiers during World War II. The movie uses an intense non-linear storytelling style and focuses on survival, tension, and large-scale historical events."
    ),
    Document(
        page_content="Tenet is a science fiction espionage thriller by Christopher Nolan that introduces the concept of time inversion. The film follows a secret agent trying to prevent a global catastrophe using objects and people that move backward through time."
    ),
    Document(
        page_content="Memento is a psychological thriller by Christopher Nolan about a man suffering from short-term memory loss. The story is told in reverse order, forcing the audience to piece together the events along with the main character."
    ),
]

# make the embeddings 
embeddings = OllamaEmbeddings(model="nomic-embed-text:latest")

# making vector store
vector_store = FAISS.from_documents(
    documents=documents,
    embedding=embeddings
)

k = 2
# make the retriever
retriever = vector_store.as_retriever(
    search_type="mmr", # This enables mmr
    search_kwargs={'k': k, "lambda_mult": 0.5} # k = top results, lambda_mult = relevance-diversity balance, range(0 to 1)
    # for lambda_mult = 1 it works as similar as the similarity search from the vector store, and for diverse results reduce it to 0
)

query = "In which movie there was the concept of time inversion?"

results = retriever.invoke(query)

print(f"Here's your top-{k} results:")
for i, doc in enumerate(results,1):
    print(f"{i}. {doc.page_content}")