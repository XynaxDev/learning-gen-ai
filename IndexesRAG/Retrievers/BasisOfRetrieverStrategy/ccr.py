# CCR = Contexual Compression Retriever

from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace
from langchain_community.vectorstores import FAISS
from langchain_ollama import OllamaEmbeddings
from langchain_classic.retrievers import ContextualCompressionRetriever
from langchain_classic.retrievers.document_compressors import LLMChainExtractor
from langchain_core.documents import Document
from dotenv import load_dotenv

load_dotenv()

# Docs
docs = [
    Document(
        page_content="Electric vehicles (EVs) significantly reduce greenhouse gas emissions compared to internal combustion engines because they have no tailpipe emissions.",
        metadata={"source": "environmental_report", "priority": "high"},
    ),
    Document(
        page_content="The morning sun rose over the factory where workers were busy assembling parts. While the lunch menu featured sandwiches, the lead engineer noted that EV batteries are now 85% recyclable, which is a major sustainability milestone for the industry. Many employees prefer commuting by bike.",
        metadata={"source": "factory_newsletter", "priority": "medium"},
    ),
    Document(
        page_content="The primary challenge for EV adoption remains the charging infrastructure. Most owners charge their cars at home overnight using a Level 2 charger, which takes about 4 to 8 hours for a full charge.",
        metadata={"source": "user_guide", "priority": "medium"},
    ),
    Document(
        page_content="Internal combustion engines rely on small explosions of gasoline to move pistons. These traditional vehicles require regular oil changes and spark plug replacements to maintain efficiency.",
        metadata={"source": "mechanic_blog", "priority": "low"},
    ),
    Document(
        page_content="Traditional sourdough bread requires a starter made of fermented flour and water. The process of baking a perfect loaf involves steam and high heat to achieve a crispy crust.",
        metadata={"source": "cookbook", "priority": "none"},
    ),
    Document(
        page_content="The local park will be closed for maintenance on Friday. In related news, switching to an electric fleet can reduce a city's carbon footprint by 40% over ten years. Please remember to keep your dogs on a leash.",
        metadata={"source": "city_announcement", "priority": "high"},
    ),
]

# Models
hf = HuggingFaceEndpoint(repo_id="google/gemma-2-2b-it")
model = ChatHuggingFace(llm=hf)

embeddings = OllamaEmbeddings(model="nomic-embed-text:latest")

# vector store
vector_store = FAISS.from_documents(
    documents=docs,
    embedding=embeddings
)

retriever = vector_store.as_retriever(search_kwargs={'k': 5})

# setup compressor
compressor = LLMChainExtractor.from_llm(model)

# now create a compression retriever
contextual_compression_retriever = ContextualCompressionRetriever(
    base_compressor=compressor,
    base_retriever=retriever
)


query = "What are the environmental impacts and sustainability benefits of electric vehicles?"

results = contextual_compression_retriever.invoke(query)
print("Here's your results: ")
for i, doc in enumerate(results,1):
    print(f"{i}. {doc.page_content}")