from langchain_ollama import ChatOllama
from langchain_core.prompts import PromptTemplate

llm = ChatOllama(model= "llama3.1:8b", temperature=0.5, max_tokens=500)

template = PromptTemplate(
    template= """
    Please summarize the research paper titled "{paper_title}" with the following specifications:
    Explanation Style: {explanation_style}
    Explanation Length: {explanation_length}
    1. Mathematical Details: 
        - Include relevant equations and derivations if present in the paper.
        - Explain the mathematical concepts using simple, intuitive code snippets where applicable.
    2. Analogies:
        - Use relatable analogies to clarify complex ideas.
    If certain information is not available in the paper, respond with "Insufficient information".
    Ensure the summary is clear , accurate and aligns with the specified style and length.

    """,
    input_variables=["paper_title", "explanation_style", "explanation_length"],
    validate_template=True,
)

paper_title = input("Enter the title of the research paper: ")
explanation_style = input("Enter the explanation style (e.g., simple, detailed, technical): ")
explanation_length = input("Enter the explanation length (e.g., short, medium, long): ")

prompt = template.invoke({
        "paper_title":paper_title,
        "explanation_style":explanation_style,
        "explanation_length":explanation_length
    }
)

response = llm.invoke(prompt)

print("Generated Summary:\n", response.content)