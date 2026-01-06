from langchain_experimental.text_splitter import SemanticChunker
from langchain_ollama import OllamaEmbeddings

embeddings = OllamaEmbeddings(model="nomic-embed-text")

splitter = SemanticChunker(
    embeddings=embeddings,
    breakpoint_threshold_type="standard_deviation",
    breakpoint_threshold_amount=0.9
)

text = """Artificial Intelligence is used in apps like search engines and chatbots to automate tasks that normally need human intelligence. It helps machines understand language, images, and data. As AI becomes more common, people also discuss its impact on jobs and ethics.
The universe contains stars, planets, and mysterious objects like black holes. Scientists use telescopes to study how galaxies are formed and how the universe began. Even today, much of space is still unknown.
Running a business requires planning, good decisions, and understanding customers. Many companies use technology to grow faster and reach more people. Long-term success usually comes from adapting and improving continuously.
"""

chunks = splitter.split_text(text)

print(len(chunks))
print(chunks)
