from langchain_ollama import ChatOllama
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

load_dotenv()


model = ChatOllama(model="tinyllama:1.1b", temperature=0.4, max_token=200)
# this model of hf is working u can test it as well if u dont want to run ollama in local
model_ep = HuggingFaceEndpoint(
    repo_id="google/gemma-2-2b-it", temperature=0.4, max_new_tokens=400
)
model_hf = ChatHuggingFace(llm=model_ep)

template1 = PromptTemplate(
    template="write a detailed report on {topic}", input_variables=["topic"]
)

template2 = PromptTemplate(
    template="Write five line summary on this content: \n {text}",
    input_variables=["text"],
)

# isntead of doing these we can use chains + strOutputParsers
# prompt1 = template1.format({"topic": "Balck Hole"})
# result1 = model.invoke(prompt1)
# prompt2 = template2.format({"text": result1.content})
# result2 = model.invoke(prompt2)

# print(result1.content)

parser = StrOutputParser()

# making chain because strOutputParser works better with chains
chain = template1 | model_hf | parser | template2 | model_hf | parser
# here parser is converting llm output into strings so it can be further used by llms
result = chain.invoke({"topic": "Black Hole"})

print("\nSummary: \n", result)
