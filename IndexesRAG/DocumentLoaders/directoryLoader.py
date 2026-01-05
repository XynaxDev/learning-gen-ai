from langchain_community.document_loaders import DirectoryLoader,PyPDFLoader

# loading the data
loader = DirectoryLoader(
    path="./IndexesRAG/DocumentLoaders/Books",
    glob="*.pdf",
    loader_cls=PyPDFLoader
)
# docs = loader.load()
# fetching the content
# docs_content = docs[0].page_content
# docs_metadata = docs[1].metadata

# print(docs_content,"\n")
# print(docs_metadata)
# print(len(docs))

# using lazy_load()
lazy_doc = loader.lazy_load()
for dc in lazy_doc:
    print(dc.metadata)