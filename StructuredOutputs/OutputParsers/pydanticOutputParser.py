from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import PromptTemplate
from pydantic import BaseModel, Field
from dotenv import load_dotenv

# strOutputParser: string output parser

load_dotenv()

hf = HuggingFaceEndpoint(
    repo_id="google/gemma-2-2b-it", temperature=0.7, max_new_tokens=400
)
model = ChatHuggingFace(llm=hf)

# pycdantic schema
class Person(BaseModel):
    name: str = Field(description="Name of the person")
    age: int = Field(gt=18, description="Age of the person")
    city: str = Field(description="Name of the city of the person")

parser = PydanticOutputParser(pydantic_object=Person)


template = PromptTemplate(
    template="Give me the name, age and city of any fictional character\n {format_instruction}",
    input_variables=[],
    partial_variables={"format_instruction": parser.get_format_instructions},
    validate_template=True,
)

# prompt = template.format()
# result = model.invoke(prompt)

# final_result = parser.parse(result.content)

# print(prompt)
# print(final_result)

# via chain

chain = template | model | parser

result = chain.invoke({})
print(result)