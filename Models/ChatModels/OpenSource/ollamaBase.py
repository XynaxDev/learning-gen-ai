from langchain_ollama import OllamaLLM
from dotenv import load_dotenv

load_dotenv()

# 1. Initialize the Model
llm = OllamaLLM(
    model="llama3.1:8b",  # Model you pulled
    temperature=0.7,
    # Ollama runs locally by default on http://localhost:11434
)

# 2. Simple String Query
query = "Why is the sky blue?"

# 3. Invoke directly with the string
response = llm.invoke(query)

# 4. Display Results
print(f"User Query: {query}")
print(f"AI Response: {response}")