from langchain_anthropic import ChatAnthropic
from dotenv import load_dotenv

load_dotenv()

# 1. Initialize the Model
llm = ChatAnthropic(model="claude-3-7-sonnet-20250219", temperature=0.5)

# 2. Simple String Query
query = "Explain why the sky is blue like I am five."

# 3. Invoke with just the string
response = llm.invoke(query)

# 4. Display Results
print(f"User Query: {query}")
print(f"AI Response: {response.content}")