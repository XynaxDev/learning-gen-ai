from langchain_huggingface import HuggingFaceEndpoint
from dotenv import load_dotenv
import os

load_dotenv()

# 1. Initialize the Model (Serverless API)
# repo_id is the model name from Hugging Face Hub
llm = HuggingFaceEndpoint(repo_id="mistralai/Mistral-7B-Instruct-v0.3",temperature=0.8,
		max_new_tokens=512,
    huggingfacehub_api_token=os.getenv("HUGGINGFACE_API_TOKEN")
)

# 2. Simple String Query
query = "What are the benefits of open-source AI?"

# 3. Invoke with just the string
response = llm.invoke(query)

# 4. Display Results
print(f"User Query: {query}")
print(f"AI Response: {response}")