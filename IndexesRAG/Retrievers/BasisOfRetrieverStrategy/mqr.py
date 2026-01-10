# MQR = Multi Query Retrieval

from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_classic.retrievers import (
    MultiQueryRetriever,
)  # 1st -> pip install langchain-classic
from langchain_core.documents import Document
from langchain_ollama import ChatOllama
from langchain_core.prompts import PromptTemplate
from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace
from dotenv import load_dotenv

load_dotenv()

# 1. make the docs
all_docs = [
    # --- Health & Wellness (Target Documents) ---
    Document(
        page_content="Regular walking boosts heart health and can reduce symptoms of depression.",
        metadata={"source": "H1"},
    ),
    Document(
        page_content="Consuming leafy greens and fruits helps detox the body and improve longevity.",
        metadata={"source": "H2"},
    ),
    Document(
        page_content="Deep sleep is crucial for cellular repair and emotional regulation.",
        metadata={"source": "H3"},
    ),
    Document(
        page_content="Mindfulness and controlled breathing lower cortisol and improve mental clarity.",
        metadata={"source": "H4"},
    ),
    Document(
        page_content="Drinking sufficient water throughout the day helps maintain metabolism and energy.",
        metadata={"source": "H5"},
    ),
    Document(
        page_content="Yoga and Tai Chi are excellent for improving physical balance and mental focus.",
        metadata={"source": "H6"},
    ),
    Document(
        page_content="High-protein snacks can provide a quick boost of energy during long work hours.",
        metadata={"source": "H7"},
    ),
    # --- Keyword Traps (Irrelevant Documents) ---
    Document(
        page_content="The solar energy system in modern homes helps balance electricity demand.",
        metadata={"source": "I1"},
    ),
    Document(
        page_content="Python balances readability with power, making it a popular system design language.",
        metadata={"source": "I2"},
    ),
    Document(
        page_content="Photosynthesis enables plants to produce energy by converting sunlight.",
        metadata={"source": "I3"},
    ),
    Document(
        page_content="The 2022 FIFA World Cup was held in Qatar and drew global energy and excitement.",
        metadata={"source": "I4"},
    ),
    Document(
        page_content="Black holes bend spacetime and store immense gravitational energy.",
        metadata={"source": "I5"},
    ),
]

# 2. Embedding model
embeddings = OllamaEmbeddings(model="nomic-embed-text:latest")

# 3. making vector store
vector_store = FAISS.from_documents(documents=all_docs, embedding=embeddings)

# Note: for improvements in the retrieval 
QUERY_PROMPT = PromptTemplate(
    input_variables=["question"],
    template="""You are an AI language model assistant. Your task is to generate five 
    different versions of the given user query to retrieve relevant documents from a vector 
    database. By generating multiple perspectives on the user query, your goal is to help
    the user overcome some of the limitations of the distance-based similarity search. 
    
    Provide these alternative questions separated by newlines.
    Do not include any introductory text, numbers, or explanations. 
    Focus strictly on human health and wellness.

    Original question: {question}""",
)

# 4. Creating both retrievers: similarity and the Multiquery
hf = HuggingFaceEndpoint(repo_id="google/gemma-2-2b-it")
model = ChatHuggingFace(llm=hf)

similarity_retriever = vector_store.as_retriever(
    search_type="similarity", 
    search_kwargs={"k": 5}
)
multiquery_retriever = MultiQueryRetriever.from_llm(
    retriever=vector_store.as_retriever(search_kwargs={"k": 5}), 
    llm=model,
    prompt=QUERY_PROMPT
)

# 5. Query (Ambiguous)
query = "How to improve energy levels and maintain balance?"

similarity_results = similarity_retriever.invoke(query)
multiquery_results = multiquery_retriever.invoke(query)

print("Here's your top 5 similarity based results: ")
for i, doc in enumerate(similarity_results, 1):
    print(f"{i}. {doc.page_content}")


print("\nHere's your top 5 multiquery based results: ")
for i, doc in enumerate(multiquery_results, 1):
    print(f"{i}. {doc.page_content}")

# Note: here the MQR is also failing the semantic retrieval because of the llm which is generating the queries from the user query is drifting" because the word "balance" and "energy" are polysemous (they have multiple meanings)
# Without specific instructions, the LLM generated variations that accidentally triggered your "keyword traps."

# Here we can improve that by imposing some instructions to the model using prompts
# see line 76