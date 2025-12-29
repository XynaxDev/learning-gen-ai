from langchain_huggingface import HuggingFacePipeline
from dotenv import load_dotenv

load_dotenv()

# 1. Initialize the Local Model
# from_model_id downloads the model and creates a local pipeline
llm = HuggingFacePipeline.from_model_id(
    model_id="gpt2", # Using a small model (gpt2) so it runs fast locally
    task="text-generation",
    pipeline_kwargs={"max_new_tokens": 100, "temperature": 0.7}
)

# 2. Simple String Query
query = "The future of artificial intelligence is"

# 3. Invoke locally
response = llm.invoke(query)

# 4. Display Results
print(f"User Query: {query}")
print(f"AI Response: {response}")