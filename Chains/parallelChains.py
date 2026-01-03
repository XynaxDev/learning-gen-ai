from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from langchain_ollama import ChatOllama
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel
from langchain_core.runnables.graph import MermaidDrawMethod # for viz
from dotenv import load_dotenv
load_dotenv()

hf = HuggingFaceEndpoint(
    repo_id="google/gemma-2-2b-it", temperature=0.5
)
model1 = ChatHuggingFace(llm=hf)
model2= ChatOllama(model="llama3.2:3b",temperature=0.5)

prompt1 = PromptTemplate(
    template="Generate simple and conscise notes out of this given text\n {text}",
    input_variables=['text']
)

prompt2 = PromptTemplate(
    template="Generate 5 short question and answer from the given text \n {text}",
    input_variables=['text']
)

prompt3 = PromptTemplate(
    template="Merge the provided notes and quiz in one single document \n notes: {notes} \n Quiz: {quiz}",
    input_variables=['notes','quiz']
)

topic = """
    What Are Transformers in Machine Learning?
    Transformers are deep learning models introduced in the groundbreaking paper “Attention is All You Need” by Vaswani et al. in 2017, unlike traditional models such as recurrent neural networks (RNNs) and long short-term memory networks (LSTMs), transformers process input data all at once, rather than sequentially. This key innovation enables them to handle long-range dependencies in data with remarkable efficiency. 

    Key Concepts of Transformers
    Self-Attention Mechanism: At the heart of transformers lies the self-attention mechanism. This allows the model to weigh the relevance of different words in a sequence relative to each other, regardless of their position. 
    For instance, consider a supply chain management scenario where a retailer needs to predict delays in product delivery. In this context, the relationship between “shipment delay” and “supplier performance” might be more significant than the link between “inventory levels” and “supplier performance.” Self-attention mechanisms in transformers enable the model to weigh these relationships dynamically, identifying that “shipment delay” has a higher relevance to “supplier performance,” which in turn informs better decision-making in supply chain operations.

    Encoder-Decoder Structure: The transformer architecture consists of two main components:
    Encoder: Processes input data and generates a rich, contextualized representation by capturing relationships between all elements in the input sequence. This is achieved through multiple layers of self-attention and feed-forward networks, where each layer refines the representation by attending to different aspects of the input. For example, in a machine translation task, the encoder can focus on understanding the grammatical structure and meaning of the input sentence in the source language.

    Decoder: Uses this representation to generate the output sequence, such as translated text or predicted tokens, step by step as shown in the figure below. It achieves this by attending both to the encoder’s output and to its own previously generated tokens, ensuring that the generated output remains coherent and contextually accurate. For instance, in text summarization, the decoder iteratively refines its output to create a concise yet meaningful summary of the input text.
"""

parser = StrOutputParser()

# for the parallel chains we always need a runnable parallel
parallel_chains = RunnableParallel({
    'notes': prompt1 | model1 | parser,
    'quiz': prompt2 | model2 | parser
})

# now merging bot the parallel chains
merge_chains = prompt3 | model2 | parser

# now by combining these both parallel and merged chain make a final chain
chain = parallel_chains | merge_chains
result = chain.invoke({
    'text': topic
})

print(result)

chain.get_graph().print_ascii()
# viz part 
mermaid_png = chain.get_graph().draw_mermaid_png(
    draw_method=MermaidDrawMethod.API
)
# Save to file
with open("chain_graph.png", "wb") as f:
    f.write(mermaid_png)

print("Graph saved as chain_graph.png!")