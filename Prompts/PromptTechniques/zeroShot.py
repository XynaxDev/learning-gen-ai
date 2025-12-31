from langchain_ollama import ChatOllama

llm = ChatOllama(model="llama3.2:3b", temperature=0.3)

prompt = """You are a sentiment analysis expert.
    Classify the following sentences into "Positive", "Negative", or "Neutral" sentiments.
    Provide one-word answers only.

    1. I am feeling amazing today!
    2. I don't want to go out and play right now.
    3. I will read an article instead.
"""

response = llm.invoke(prompt)
print(response.content)