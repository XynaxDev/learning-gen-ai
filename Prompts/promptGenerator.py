from langchain_core.prompts import PromptTemplate

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

template.save("prompts/research_paper_summary_prompt.json")