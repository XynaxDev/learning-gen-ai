from langchain_ollama import ChatOllama
from pydantic import BaseModel, Field
from typing import Literal, Optional

model = ChatOllama(model="llama3.2:3b", temperature=0.5)

review = "I went into this movie with fairly normal expectations, and honestly, that’s probably why it worked so well for me. The story itself isn’t something you’ve never seen before, but it’s told with enough sincerity that you don’t mind the familiar beats. The first half takes its time setting things up — maybe a little too much for some — but once the conflict kicks in, the film finds its rhythm and stays there till the end. The performances are a major highlight. You may not walk out calling it a masterpiece, but it stays with you longer than expected. Overall, this is a well-made film that understands its strengths and doesn’t pretend to be something it’s not. Definitely worth a watch if you enjoy character-driven stories with heart."

review_complex = """I recently switched to the Samsung Galaxy S24 Ultra, and overall, it’s an absolute beast of a smartphone. The Snapdragon 8 Gen 3 chipset keeps everything extremely smooth—whether it’s heavy multitasking, gaming, or photo editing. The 5000mAh battery comfortably gets me through an entire day of intense usage, and the 45W fast charging really comes in handy when I’m low on time.
    The built-in S-Pen is a nice bonus for jotting down notes or quick sketches, even though I don’t use it daily. The real standout for me is the 200MP camera—the night mode performs exceptionally well, delivering sharp and vibrant shots even in low-light conditions. The zoom is impressive too; up to around 30x it’s very usable, though anything closer to 100x does start to lose clarity.

    That said, the phone’s size and weight make it slightly awkward to use with one hand for long periods. On top of that, Samsung’s One UI still includes unnecessary pre-installed apps—having multiple Samsung alternatives for things Google already does well feels redundant. The $1,300 price tag also makes it a tough purchase to justify for everyone.

    Pros:
    Extremely powerful processor (excellent for gaming and productivity)
    Impressive 200MP camera with strong zoom performance
    Reliable all-day battery life with fast charging
    S-Pen functionality is distinctive and genuinely useful

    Cons:
    Large and heavy—not ideal for one-handed use
    Extra apps and bloatware still present in One UI
    High price compared to rival flagship phones
    
    Review by akash kumar
"""


class Review(BaseModel):
    summary: str = Field(description="A brief summary of the review!")
    sentiment: Literal["pos","neg"] = Field(description="Return sentiment of the review either negative, positive")

# Pydantic Scehema
class ReviewComplex(BaseModel):
    key_features: list[str] = Field(description="Write down all the key features mentioned in the review")
    summary: str = Field(description="A brief summary of the review!")
    sentiment: Literal["pos","neg"] = Field(description="Return sentiment of the review either negative, positive")
    pros: Optional[list[str]] = Field(description="write down all the pros in the list.")
    cons: Optional[list[str]] = Field(description="write down all the cons in the list.")
    reviewer_name:Optional[str] = Field(description="Write the name of the reviewer")



# Normal Review
# str_out_llm = model.with_structured_output(Review)

# result = str_out_llm.invoke(review)
# print(result)
# print("\n Summary: ", result["summary"])
# print("\n Sentiment: ", result["sentiment"])

# Complex Review
str_out_llm = model.with_structured_output(ReviewComplex)

result = str_out_llm.invoke(review_complex)
dict_result = result.model_dump() # to dict

# to access pydantic object vals just do as u do  while calling class object using dot operator
# print(result.summary)

print(dict_result)
print("\n Key features: ", dict_result["key_features"])
print("\n Summary: ", dict_result["summary"])
print("\n Sentiment: ", dict_result["sentiment"])