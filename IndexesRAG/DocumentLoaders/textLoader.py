from langchain_community.document_loaders import TextLoader
from langchain_ollama import ChatOllama
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda

model = ChatOllama(model="llama3.2:3b", temperature=0.6)

prompt = PromptTemplate(
    template="Summarize the given text with their key concepts: {text}",
    input_variables=['text']
)

parser = StrOutputParser()

# loading the data
loader = TextLoader("./IndexesRAG/DocumentLoaders/nolan.txt", encoding='utf-8')
docs = loader.load()
# fetching the content
docs_content = docs[0].page_content

chain = prompt | model | parser

summary = chain.invoke({'text': docs_content})

print(summary)