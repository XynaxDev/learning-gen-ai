from langchain_ollama import ChatOllama
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableSequence,RunnableParallel, RunnablePassthrough, RunnableLambda
from langchain_core.output_parsers import StrOutputParser

llm = ChatOllama(model="llama3.2:3b")

# runnable lambda is very powerfull
def word_count(text):
    return len(text.split())


prompt1 = PromptTemplate(
    template="Generate me a fantasy joke on this topic {topic}",
    input_variables=['topic']
)


parser = StrOutputParser()

joke_chain = RunnableSequence(prompt1, llm, parser)

paralell_chain = RunnableParallel({
    'joke': RunnablePassthrough(),
    'word_count': RunnableLambda(word_count),
    # or u can use lambda fn 
    # 'word_count': RunnableLambda(lambda x: len(x.split())) 
})

final_chain = RunnableSequence(joke_chain, paralell_chain)

res = final_chain.invoke({'topic': 'Christopher Nolan'})

print(f"""Here is the Joke: {res['joke']}\n Total word count: {res['word_count']}
"""
)