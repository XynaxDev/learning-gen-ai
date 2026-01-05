from langchain_ollama import ChatOllama
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableSequence,RunnableParallel, RunnablePassthrough
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

joke_chain = RunnableSequence(template1, llm, parser)

paralell_chain = RunnableParallel({
    'joke': RunnablePassthrough(),
    'explanation': RunnableSequence(template2, llm, parser)
})

final_chain = RunnableSequence(joke_chain, paralell_chain)

res = final_chain.invoke({'topic': 'Christopher Nolan'})

print(res)