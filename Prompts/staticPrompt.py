from langchain_ollama import ChatOllama

llm = ChatOllama(model="gemma3:270m",temperature= 0.5)

while True:
    print("Enter your query (type 'exit' or 'quit' to stop):")
    user_query = input("User: ")
    if user_query.lower() in ["exit", "quit"]:
        break

    response = llm.invoke(user_query)
    print("AI:", response.content)