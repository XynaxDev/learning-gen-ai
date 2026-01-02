from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv

load_dotenv()

hf = HuggingFaceEndpoint(
    repo_id="google/gemma-2-2b-it", temperature=0.4, max_new_tokens=400
)
model = ChatHuggingFace(llm=hf)
parser = JsonOutputParser()

template = PromptTemplate(
    template="Give me the name, age and city of any fictional character\n {format_instruction}",
    input_variables=[],
    partial_variables={"format_instruction": parser.get_format_instructions},
    validate_template=True,
)

# prompt = template.format()

# result = model.invoke(prompt)

# # now parsing it using parse fn
# final_result = parser.parse(result.content)

# print(final_result)
# print(type(final_result))

# or u can use chains to do the same
chain = template | model | parser

result1 = chain.invoke({}) # use dict if not passed any input vars in the templates
print(result1)
