from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv()

# 1. Initialize the Model
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0.3)

# 2. Simple String Query
query = "Give me a 5-day study plan for learning LangChain."

# 3. Invoke with just the string
response = llm.invoke(query)

# 4. Display Results
print(f"User Query: {query}")
print(f"AI Response: {response.content}")