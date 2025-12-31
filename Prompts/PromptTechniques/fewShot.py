from langchain_ollama import ChatOllama
from langchain_core.prompts import PromptTemplate

llm = ChatOllama(model="llama3.2:3b", temperature=0.3)

template = PromptTemplate(
    template="""Classify customer emails into the correct support category.

    Examples:
    Email: "My order hasn't arrived yet. It's been 10 days!"
    Category: Delivery Issue

    Email: "I love your product! The color is perfect."
    Category: Positive Feedback

    Email: "The product quality is terrible. I want a refund immediately."
    Category: Product Issue

    Email: "Can you help me choose the right size for my body type?"
    Category: Sales Support

    Email: "Your website keeps crashing when I try to checkout."
    Category: Technical Issue

    Now classify this email:
    Email: "{email_text}"
    Category:""",
    input_variables=["email_text"],
)

# Test cases
test_emails = [
    "I received the wrong item in my package.",
    "How do I return a product I don't need?",
    "The app won't let me log in after the update.",
]

for email in test_emails:
    prompt = template.invoke({"email_text": email})
    response = llm.invoke(prompt)
    print(f"Email: {email}")
    print(f"Category: {response.content}\n")
