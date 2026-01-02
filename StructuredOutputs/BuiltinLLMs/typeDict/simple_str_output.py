from langchain_ollama import ChatOllama
from typing import TypedDict

model = ChatOllama(model="llama3.2:3b", temperature=0.7)

review = "I went into this movie with fairly normal expectations, and honestly, that’s probably why it worked so well for me. The story itself isn’t something you’ve never seen before, but it’s told with enough sincerity that you don’t mind the familiar beats. The first half takes its time setting things up — maybe a little too much for some — but once the conflict kicks in, the film finds its rhythm and stays there till the end. The performances are a major highlight. You may not walk out calling it a masterpiece, but it stays with you longer than expected. Overall, this is a well-made film that understands its strengths and doesn’t pretend to be something it’s not. Definitely worth a watch if you enjoy character-driven stories with heart."


class Review(TypedDict):
    summary: str
    sentiment: str


structured_output_llm = model.with_structured_output(Review)

result = structured_output_llm.invoke(review)

print(result)
print("\n Summary: ", result["summary"])
print("\n Sentiment: ", result["sentiment"])