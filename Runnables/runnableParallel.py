from langchain_ollama import ChatOllama
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableSequence, RunnableParallel
from langchain_core.output_parsers import StrOutputParser

llm = ChatOllama(model="llama3.2:3b")

prompt1 = PromptTemplate(
    template="Generate me a tweet about this topic {topic}",
    input_variables=['topic']
)

prompt2 = PromptTemplate(
    template="Generate me a linkedin post about this topic {topic}",
    input_variables=['topic']
)

parser = StrOutputParser()

parallel_chain = RunnableParallel({
    'tweet': RunnableSequence(prompt1, llm, parser),
    'linkedin': RunnableSequence(prompt2, llm, parser)
})

result = parallel_chain.invoke({'topic': 'Christopher Nolan'})
print(result)
print("\n")
print(result["tweet"])
print("\n")
print(result["linkedin"])

