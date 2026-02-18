# Using Base Tool: It is the abstract base class for all tools in Langchain. It defines the core structure and interface that any tool must follow, whether its simple one liner or a fully  customized func

# All tools like @tool or structuredTool are built on this base model

from langchain.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Type

# arg schema using pydantic

class MultiplyInput(BaseModel):
    a: int = Field(description="The first number to add")
    b: int = Field(description="The second number to add")

# now its actually a tool which is inheriting the BaseTool model
class MultiplyTool(BaseTool):
    name: str = "multiply"
    description: str = "Multiply two numbers"

    args_schema: Type[BaseModel] = MultiplyInput

    def _run(self, a: int, b: int) -> int:
        return a * b
    

multiply_tool = MultiplyTool()
result = multiply_tool.invoke({"a": 3, "b": 6})
print(result)

print(multiply_tool.name)
print(multiply_tool.args)
print(multiply_tool.description)
