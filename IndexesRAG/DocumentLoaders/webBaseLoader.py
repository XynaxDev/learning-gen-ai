from langchain_community.document_loaders import WebBaseLoader
from langchain_ollama import ChatOllama
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

model = ChatOllama(model="llama3.2:3b", temperature=0.6)

prompt = PromptTemplate(
    template="You are a helpful AI assistant and your task is to answer this query {query} on this given text:\n{text}",
    input_variables=['query','text']
)

parser = StrOutputParser()

# loading the data
url = "https://www.amazon.in/soundcore-Cancelling-Headphones-Bluetooth-Transparency/dp/B0CQXMXJC5/?_encoding=UTF8&pd_rd_w=Bs7CL&content-id=amzn1.sym.ed223e70-d8c8-4549-9e85-87f039655f35&pf_rd_p=ed223e70-d8c8-4549-9e85-87f039655f35&pf_rd_r=4TQ40THDA23Z91B9NTT2&pd_rd_wg=CAgSE&pd_rd_r=5b9f56b1-b49e-4b26-a271-e995d516a8b5&ref_=pd_hp_d_atf_dealz_sv&th=1"
loader = WebBaseLoader(url) # u can pass list of urls here and that will return as much document object you want
docs = loader.load()
# fetching the content
docs_content = docs[0].page_content

chain = prompt | model | parser

about = chain.invoke({'query':'Tell me which product is this? and what is the price?', 'text': docs_content})

print(about)
print(docs[0].metadata)