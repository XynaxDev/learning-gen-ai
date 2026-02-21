from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, AIMessage
from langchain.chat_models import init_chat_model
from os import getenv
from dotenv import load_dotenv
load_dotenv()

# Initialize the model with OpenRouter's base URL
open_router_model = init_chat_model(
    model="z-ai/glm-4.5-air:free",
    model_provider="openai",
    base_url="https://openrouter.ai/api/v1",
    api_key=getenv("OPENROUTER_API_KEY"),
)


# tool create
@tool
def multiply(a: int, b: int) -> int:
  """Given 2 numbers a and b this tool returns their product"""
  return a * b

# print(multiply.invoke({'a':3, 'b':4}))
# print(multiply.name)
# print(multiply.description)
# print(multiply.args)

# tool binding 
binded_tools = open_router_model.bind_tools([multiply])
query = HumanMessage('can you multiply 3 with 500')
messages = [query]
# print(binded_tools)

# tool execution
result = binded_tools.invoke(messages)
messages.append(result)

# tool_result = multiply.invoke(result.tool_calls[0]['args'])
tool_result = multiply.invoke(result.tool_calls[0])
messages.append(tool_result)
# print(messages)

final_response = open_router_model.invoke(messages)
print(final_response.content)