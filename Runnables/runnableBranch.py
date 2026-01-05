from langchain_ollama import ChatOllama
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableSequence,RunnableBranch
from pydantic import BaseModel, Field
from typing import Literal
from langchain_core.output_parsers import PydanticOutputParser, StrOutputParser

llm = ChatOllama(model="llama3.2:3b", temperature=0)


class emailReader(BaseModel):
    email_type: Literal["Complain email", "Refund email", "General email"] = Field(
        description="classify it into Complain email, Refund email or General query email."
    )


parser = PydanticOutputParser(pydantic_object=emailReader)

prompt = PromptTemplate(
    template="""
        You will analyze the email below and classify it into one of:
        "Complain email", "Refund email", "General email".

        Email:
        {email}

        IMPORTANT:
        - Return ONLY a single valid JSON object (no markdown, no code fences, no extra text).
        - Do NOT repeat the schema or the format instructions.
        - If you fail to follow the rules, the response will be rejected.

        FORMAT INSTRUCTIONS (do not repeat these lines, only produce the JSON):
        {formated_instruction}

        Example expected output exactly like this:
        {{"email_type":"Complain email"}}
""",
    input_variables=["email"],
    partial_variables={"formated_instruction": parser.get_format_instructions()},
)

prompt_complain = PromptTemplate(
    template="""
        You are a customer support complaint-handling agent.

        Your task:
        - Read the incoming email carefully.
        - Acknowledge the customer’s issue politely.
        - Apologize briefly for the inconvenience.
        - Assure the customer that the issue will be reviewed and resolved.
        - Do NOT invent order numbers, refunds, or timelines.

        Incoming email:
        {email}

        Write a clear, professional response email.
""",
    input_variables=["email"],
)

prompt_refund = PromptTemplate(
    template="""
        You are a customer support refund-handling agent.

        Your task:
        - Read the incoming email carefully.
        - Acknowledge the refund request.
        - Explain the refund process in a neutral and professional tone.
        - Ask for any required details if missing (politely).
        - Do NOT promise immediate refunds or specific amounts.

        Incoming email:
        {email}

        Write a clear, professional response email.
""",
    input_variables=["email"],
)

prompt_general = PromptTemplate(
    template="""
        You are a customer support general-query agent.

        Your task:
        - Understand the customer’s question.
        - Provide a helpful and concise response.
        - Keep the tone polite and informative.
        - If information is missing, ask a follow-up question clearly.

        Incoming email:
        {email}

        Write a clear, professional response email.
""",
    input_variables=["email"],
)


parser2 = StrOutputParser()

email = """Hello Team,

I am writing to report an issue with my recent order. The product I received is not working as expected.

Please look into this matter and let me know how it can be resolved at the earliest.

Thank you,
Akash Kumar
"""

analyse_chain = RunnableSequence(prompt, llm, parser)

branch_chain = RunnableBranch(
    (lambda x: x.email_type == "Complain email", RunnableSequence(prompt_complain, llm, parser2)),
    (lambda x: x.email_type == "Refund email",RunnableSequence(prompt_refund, llm, parser2)),
    RunnableSequence(prompt_general, llm, parser2),
)

final_chain = RunnableSequence(analyse_chain, branch_chain)

final_res = final_chain.invoke({"email": email})

print(final_res)
final_chain.get_graph().print_ascii()