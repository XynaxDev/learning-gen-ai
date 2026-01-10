from langchain_community.vectorstores import Chroma # pip install chromadb
from langchain_ollama import OllamaEmbeddings
from langchain_core.documents import Document

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

# 2. Initialise Embedding model
embeddings = OllamaEmbeddings(model="nomic-embed-text:latest")

# 3. Create vector store and store docs
vector_store = Chroma.from_documents(
    documents=documents,
    embedding = embeddings,
    collection_name="test-collection"
)

# 4. Convert vector store into retriever
k = 2
retriver = vector_store.as_retriever(search_kwargs= {"k": k}) # its like top_k_results, it will fetch top 2 relevant docs from the vector store

query = "Christopher Nolan film exploring dream levels and reality"
results = retriver.invoke(query)

print(f"Here's your top-{k} results:")
for i, doc in enumerate(results, 1):
    print(f"{i}. {doc.page_content}")
