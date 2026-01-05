from langchain_ollama import ChatOllama
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableSequence
from langchain_core.output_parsers import StrOutputParser

llm = ChatOllama(model="llama3.2:3b")

template1 = PromptTemplate(
    template="Generate me a fantasy joke on this topic {topic}",
    input_variables=['topic']
)

template2 = PromptTemplate(
    template="Expalain the following joke\n {joke}",
    input_variables=['joke']
)

parser = StrOutputParser()

chain = RunnableSequence(template1, llm, parser, template2, llm, parser)

res = chain.invoke({'topic': 'Christopher Nolan'})
print(res)