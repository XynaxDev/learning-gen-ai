from langchain_ollama import ChatOllama
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import AIMessage,HumanMessage
import os

from dotenv import load_dotenv
load_dotenv()

llm = ChatOllama(model="llama3.2:3b",temperature= 1.5)
# ggl = ChatGoogleGenerativeAI(model= "gemini-3-flash-preview", temperature = 1.2,max_output_tokens=300)

# Chat template
chat_template = ChatPromptTemplate([
    ("system", "You are a helpful customer support assistant of Amazon company!"),
    MessagesPlaceholder(variable_name='chat_history'), # this will load and give the chat history to the model along with user query
    ("human", "{query}")
])

# load chat history
chat_history = []

while True:
    print("Enter your query (type 'exit' or 'quit' to stop):")
    user_query = input("User: ")
    if user_query.lower() in ["exit", "quit"]:
        break


    prompt = chat_template.invoke({
        'query': user_query,
        'chat_history':chat_history
    })
    
    response = llm.invoke(prompt)
    chat_history.append(HumanMessage(content=user_query))
    chat_history.append(AIMessage(content=response.content))
    print("AI:", response.content)
    
print(chat_history)