from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from dotenv import load_dotenv
from typing import List
from datetime import datetime

load_dotenv()

app = FastAPI()

# Allow frontend calls
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

llm = ChatOllama(
    model="llama3.2:3b",
    temperature=1.2
)

messages = [
    SystemMessage(content="You are a helpful AI assistant and Akash(your creator) has made you, Answer only AI related questions , if user asks anything extra do tell them, I can't provide answer for that query You can ask me about AI!")
] 

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    reply: str
    timestamp: str

@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    messages.append(HumanMessage(content=req.message))
    response = llm.invoke(messages)
    messages.append(AIMessage(content=response.content))
    return {
        "reply": response.content,
        "timestamp": datetime.now().isoformat()
    }

@app.get("/health")
def health_check():
    return {"status": "online", "model": "llama3.2:3b"}