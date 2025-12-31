from langchain_ollama import ChatOllama

llm = ChatOllama(model="llama3.1:8b", temperature=0.2)

prompt = """Solve this problem step by step:
    A store has a sale: "Buy 2, Get 1 Free" on items priced at $15 each.
    If I want to buy 7 items, how much will I pay in total?

    Think through each step before giving the final answer.
"""

response = llm.invoke(prompt)
print(response.content)
