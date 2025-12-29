from langchain_ollama import ChatOllama
from dotenv import load_dotenv

load_dotenv()

# 1. Initialize the Chat Model
llm = ChatOllama(model="llama3.1:8b", temperature=0.6)

# 2. Simple String Query
query = "How do I read a CSV file in Python?"

# 3. Get the Response
response = llm.invoke(query)

# 4. Display the results clearly
print(f"User Query: {query}")
print(f"AI Response: {response.content}")