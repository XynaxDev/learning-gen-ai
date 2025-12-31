from langchain_ollama import ChatOllama
from langchain_core.prompts import PromptTemplate

llm = ChatOllama(model="llama3.2:3b", temperature=0.3)

template = PromptTemplate(
    template="""Extract the product name and price from the following text.

Example:
Text: "The Apple iPhone 15 Pro is available for $999"
Output: {{"product": "Apple iPhone 15 Pro", "price": "$999"}}

Now extract from this:
Text: "{input_text}"
Output:""",
    input_variables=["input_text"],
)

# Test with new input
prompt = template.invoke(
    {"input_text": "Buy the Samsung Galaxy S24 Ultra now at just $1199!"}
)

response = llm.invoke(prompt)
print(response.content)
