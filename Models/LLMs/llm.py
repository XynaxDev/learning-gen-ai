from langchain_openai import OpenAI

from dotenv import load_dotenv
load_dotenv()

# Initialize LLM with specific parameters
llm = OpenAI(model='gpt-3.5-turbo-instruct',temperature=0.7, max_tokens=150)

# Simple text completion
query = "What is the capital of India"
response = llm.invoke(query)

print(f"User Query: {query}")
print(f"AI Response: {response}")