from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
load_dotenv()

hf = HuggingFaceEndpoint(
    repo_id="google/gemma-2-2b-it", temperature=0.7, max_new_tokens=400
)

model = ChatHuggingFace(llm=hf)

prompt1 = PromptTemplate(
    template="Give me a detailed information about this topic {topic}",
    input_variables=['topic']
)

prompt2 = PromptTemplate(
    template="Give me 5 interesting facts out of this detailed information\n {info}",
    input_variables=['info']
)

# now initializing parser
parser = StrOutputParser()

chain = prompt1 | model | parser | prompt2 | model | parser

result = chain.invoke({
    'topic': 'Christopher Nolan'
})

print(result)

# the visualization of chains
chain.get_graph().print_ascii()