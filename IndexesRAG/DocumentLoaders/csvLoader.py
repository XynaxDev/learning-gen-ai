from langchain_community.document_loaders import CSVLoader
from langchain_ollama import ChatOllama
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

model = ChatOllama(model="llama3.2:3b", temperature=0.6)

prompt = PromptTemplate(
    template="You are a data analyst professional and your task is to provide mathematical analysis considering this question {quest} on the given data {data}",
    input_variables=['quest','data']
)

parser = StrOutputParser()

# loading the data
loader = CSVLoader(
    file_path="./IndexesRAG/DocumentLoaders/student_grades.csv"
)
docs = loader.lazy_load()
# print(docs)
# print(docs[0].page_content)

# fetching the content
docs_content = ""

for i, doc in enumerate(docs):
    if i >= 100:
        break
    docs_content += doc.page_content + "\n"

chain = prompt | model | parser
analysis = chain.invoke({'quest': "Tell me the top 3 scoring student among all and their student ids", 'data': docs_content})
print(analysis)