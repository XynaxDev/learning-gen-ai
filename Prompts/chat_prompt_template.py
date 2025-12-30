from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate

llm = ChatOllama(model="llama3.2:3b", temperature=1.2)

template = ChatPromptTemplate([
    ("system","You are helpful {domain} assistant."),
    ("human", "Explain in simple terms what is {topic}")
])

user_domain = input("Enter your AI domain: ")
user_topic = input("Enter topic you want to know about: ")

prompt = template.invoke({
    'domain': user_domain,
    'topic':user_topic
})

response = llm.invoke(prompt)
print(response.content)
