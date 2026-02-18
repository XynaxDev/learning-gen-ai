from langchain_community.tools import StructuredTool
from pydantic import BaseModel, Field

class MultiplyInput(BaseModel):
    a: int = Field(description="The first number to multiply")
    b: int = Field(description="The second number to multiply")


def multiply_nums(a, b): # here i dont need the type hint because the pydantic base model is doing that
    return a * b

multiply_tool = StructuredTool.from_function(
    func = multiply_nums,
    name= "multiply",
    description= "multiply two numbers",
    args_schema= MultiplyInput
)

# more matured way to use the custom tools, but most of the time wee will be using the @tool decorator 

result = multiply_tool.invoke({"a": 4,"b":7})
print(result)
print(multiply_tool.name)
print(multiply_tool.args)
print(multiply_tool.description)