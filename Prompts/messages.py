from langchain_ollama import ChatOllama
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from dotenv import load_dotenv

load_dotenv()

llm = ChatOllama(model="llama3.2:3b", temperature=1.3, max_token=300)
# ggl = ChatGoogleGenerativeAI(model= "gemini-3-flash-preview", temperature= 1.3,max_output_token=400)


# this is my model context memory
messages = [
        SystemMessage(content="You are helpful Dental assistant."),
]


while True:
    print("Enter your query here(type 'exit' to stop)")
    query = input("User: ")
    messages.append(HumanMessage(content=query))

    if query.lower() == 'exit':
        break

    # for ollama
    response = llm.invoke(messages)
    messages.append(AIMessage(content=response.content))
    print(response.content)

    # for gemini
    # response = ggl.invoke(messages)
    # messages.append(AIMessage(content=response.content[0]["text"]))
    # print(response.content[0]["text"])


print("Chat History:")
# print(messages) # either u do this or this 👇

# for msg in messages:
#     if isinstance(msg, SystemMessage):
#         print("System Messages: ",msg.content)
#     if isinstance(msg, HumanMessage):
#         print("Human Messages: ",msg.content)
#     if isinstance(msg, AIMessage):
#         print("AI Messages: ",msg.content)

# or u can extract the chat history like this
sys_msg = []
hum_msg =[]
ai_msg = []

for msg in messages:
    if isinstance(msg, SystemMessage):
        sys_msg.append(msg.content)
    if isinstance(msg, HumanMessage):
        hum_msg.append(msg.content)
    if isinstance(msg, AIMessage):
        ai_msg.append(msg.content)

print("System Messages: ", sys_msg)
print("Human Messages: ", hum_msg)
print("AI Messages: ", ai_msg)