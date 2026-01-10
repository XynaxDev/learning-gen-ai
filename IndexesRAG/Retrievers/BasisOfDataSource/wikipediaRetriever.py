from langchain_community.retrievers import WikipediaRetriever

# Initializing the retriever
retriever = WikipediaRetriever(top_k_results=2, lang="en") # here top_k_results means top k relevant results from the wikipedia on the user query

query = "Einstein Rosen Bridge"

# get the docs by using invoke fn
docs = retriever.invoke(query)

for i, doc in enumerate(docs,1):
    print(f"{i}. {doc.page_content}")