# Custom tool using @tool decorator

from langchain_community.tools import tool

# Step 1: create a function
def multiply(a,b):
    """Multiply two numbers"""
    return a * b

# Step 2: add type hints
def multiply(a: int, b: int) -> int: # this is the type hinting like here we are specifying the function so that llm can understand what is the type of arguments and what is the return type
    """Multiply two numbers"""
    return a * b

# Step 3: add tool decorator
@tool # this tool decorator is the main part it allows LLM to communicate with the custom functions
def multiply(a: int, b: int) -> int: 
    """Multiply two numbers""" # this is highly recommended to add a docstring so that llm can understand what this function does
    return a * b

# Step 4: invoke the tool
a = 2
b = 5

result = multiply.invoke({"a":a, "b":b})
print(f"The multiplication of {a} and {b} results: {result}")

print(multiply.name)
print(multiply.args)
print(multiply.description)

# the output of this line given below is what actually the llm sees, basically its the json schema which is then passed to the llm so it can understant the tool easily
print("\n{} Json Schema of the tool:")
print(multiply.args_schema.model_json_schema()) 