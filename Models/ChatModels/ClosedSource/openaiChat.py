from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

# 1. Initialize the Model
llm = ChatOpenAI(model="gpt-4o", temperature=0.7)

# 2. Simple String Query
query = "What are the three laws of robotics?"

# 3. Invoke with just the string
response = llm.invoke(query)

# 4. Display Results
print(f"User Query: {query}")
print(f"AI Response: {response.content}")