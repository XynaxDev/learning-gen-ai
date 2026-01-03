from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
load_dotenv()

hf = HuggingFaceEndpoint(
    repo_id="google/gemma-2-2b-it", temperature=0.7, max_new_tokens=400
)

model = ChatHuggingFace(llm=hf)

prompt = PromptTemplate(
    template="Write 5 interesting facts about this topic {topic}",
    input_variables=['topic']
)

parser = StrOutputParser()

chain = prompt | model | parser

result = chain.invoke({'topic': 'Chrishtopher Nolan'})
print(result)

chain.get_graph().print_ascii() # to visualise the chains