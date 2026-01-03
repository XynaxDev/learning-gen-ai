from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel, ValidationError
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from langchain_ollama import ChatOllama
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel
from dotenv import load_dotenv
import os
import json
import base64
from typing import List, Dict, Any

load_dotenv()

app = FastAPI(
    title="AI Study Assistant",
    description="Generate study materials with notes and quizzes using LangChain",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
BASE_DIR = Path(__file__).resolve().parent
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")

class TopicRequest(BaseModel):
    text: str
    use_local_ollama: bool = True

class QuizQuestion(BaseModel):
    """Structured quiz question with 4 options.

    The `answer` field must be exactly one of the `options`.
    """

    question: str
    options: List[str]
    answer: str

class StudyMaterial(BaseModel):
    notes: str
    quiz: List[QuizQuestion]
    merged_content: str
    visualization: str
    mermaid_code: str

# Initialize models
def get_models(use_local=True):
    if use_local:
        # Use smaller model to avoid memory issues
        model1 = ChatOllama(model="llama3.2:3b", temperature=0.5)
        model2 = ChatOllama(model="llama3.2:3b", temperature=0.5)
    else:
        hf = HuggingFaceEndpoint(
            repo_id="google/gemma-2-2b-it", 
            temperature=0.5,
            huggingfacehub_api_token=os.getenv("HUGGINGFACEHUB_API_TOKEN")
        )
        model1 = ChatHuggingFace(llm=hf)
        model2 = ChatHuggingFace(llm=hf)
        # model2 = ChatOllama(model="llama3.2:3b", temperature=0.5)
    
    return model1, model2

def generate_options(correct_answer: str) -> List[str]:
    options = [correct_answer]
    distractors = [
        "None of the above",
        "All of the above",
        "Not mentioned in the text",
        "An unrelated statement",
    ]
    for d in distractors:
        if len(options) >= 4:
            break
        options.append(d)
    return options[:4]

def parse_quiz_from_qa_text(raw_quiz: str) -> List[QuizQuestion]:
    questions: List[QuizQuestion] = []
    lines = raw_quiz.strip().split("\n")
    current_question = None
    current_answer = None

    for line in lines:
        text = line.strip()
        if not text:
            continue
        if text.lower().startswith("q"):
            if current_question and current_answer:
                options = generate_options(current_answer)
                questions.append(
                    QuizQuestion(question=current_question, options=options, answer=current_answer)
                )
            current_question = text.split(":", 1)[-1].strip() if ":" in text else text
            current_answer = None
        elif text.lower().startswith("a"):
            current_answer = text.split(":", 1)[-1].strip() if ":" in text else text

    if current_question and current_answer:
        options = generate_options(current_answer)
        questions.append(QuizQuestion(question=current_question, options=options, answer=current_answer))

    return questions[:5]

def parse_quiz_from_llm(raw_quiz: str) -> List[QuizQuestion]:
    text = raw_quiz.strip()
    if text.startswith("```"):
        lines = text.splitlines()
        if len(lines) >= 2:
            lines = lines[1:]
        if lines and lines[-1].strip().startswith("```"):
            lines = lines[:-1]
        text = "\n".join(lines).strip()

    try:
        data: Any = json.loads(text)
    except json.JSONDecodeError:
        return parse_quiz_from_qa_text(raw_quiz)

    if isinstance(data, dict) and "questions" in data:
        items = data["questions"]
    else:
        items = data

    if not isinstance(items, list):
        return parse_quiz_from_qa_text(raw_quiz)

    quiz: List[QuizQuestion] = []
    for item in items:
        try:
            q = QuizQuestion.model_validate(item)
            if len(q.options) != 4 or q.answer not in q.options:
                continue
            quiz.append(q)
        except ValidationError:
            continue

    if not quiz:
        return parse_quiz_from_qa_text(raw_quiz)

    return quiz[:5]

@app.get("/")
async def read_root():
    return FileResponse(BASE_DIR / "static" / "index.html")

@app.post("/generate", response_model=StudyMaterial)
async def generate_study_material(request: TopicRequest):
    try:
        print(f"Starting generation for topic: {request.text[:50]}...")
        model1, model2 = get_models(request.use_local_ollama)
        
        # Define prompts
        prompt1 = PromptTemplate(
            template="""You are an expert teacher. Read the text and write clean, well-structured, ELABORATE MARKDOWN study notes.

Follow this structure and REPLACE any bracketed instructions with real content (do NOT leave any [placeholders]):

# Study Notes

## Overview
Write 2-3 sentences explaining the main idea of the text in simple, friendly language.

## Key Concepts
- **Concept 1**: clear definition and short explanation with 1-2 real examples
- **Concept 2**: clear definition and short explanation with 1-2 real examples
- **Concept 3**: clear definition and short explanation with 1-2 real examples

## Important Points
- key point 1 with 2-3 sentences of detail
- key point 2 with 2-3 sentences of detail
- key point 3 with 2-3 sentences of detail

## How It Works (Step-by-step intuition)
Explain the idea in 3-6 short, numbered steps so that a beginner can follow the flow.

## Summary
1 short paragraph (3-4 sentences) with the main takeaways and when to use this concept.

## Recommended Resources
Provide 3-5 bullet points with helpful external resources. For each item:
- mention what the learner will understand from it
- include a YouTube SEARCH link of the form: https://www.youtube.com/results?search_query=... where the query is relevant to this topic (for example, tutorials, visual explanations or lectures)

The resources should be directly related to the topic described in the text.

Text: {text}""",
            input_variables=["text"],
        )

        # Ask the LLM to return strict JSON that we can validate with Pydantic
        prompt2 = PromptTemplate(
            template="""You are a quiz generator. From the given text, create EXACTLY 5 multiple-choice questions.

Return ONLY valid JSON in the following format (no explanations, no extra keys):

[
  {{
    "question": "...",
    "options": ["option A", "option B", "option C", "option D"],
    "answer": "one of the options exactly"
  }},
  ... 5 items total ...
]

Requirements:
- "options" must contain exactly 4 short options.
- "answer" must be exactly one of the 4 options.
- Questions and options must be concise and directly related to the text.

Text: {text}""",
            input_variables=["text"],
        )
        
        prompt3 = PromptTemplate(
            template="Merge the provided notes and quiz into one well-formatted study document.\n\nNotes:\n{notes}\n\nQuiz:\n{quiz}",
            input_variables=['notes','quiz']
        )
        
        parser = StrOutputParser()
        
        # Build chains
        parallel_chains = RunnableParallel({
            'notes': prompt1 | model1 | parser,
            'quiz': prompt2 | model2 | parser
        })
        
        merge_chains = prompt3 | model2 | parser
        chain = parallel_chains | merge_chains
        
        # Generate content with progress indication
        print("Generating notes and quiz in parallel...")
        parallel_result = parallel_chains.invoke({"text": request.text})
        notes = parallel_result["notes"]
        quiz_raw = parallel_result["quiz"]
        print(" Notes and quiz generated")

        # Parse quiz into structured, validated format
        quiz_items = parse_quiz_from_llm(quiz_raw)
        
        # Generate merged content (use original text outputs)
        print("Merging content...")
        merged = merge_chains.invoke({"notes": notes, "quiz": quiz_raw})
        
        print(" Content merged")
        
        # Generate visualization
        print("Generating visualization...")
        mermaid_code = chain.get_graph().draw_mermaid()
        
        # Remove PNG generation - only return mermaid code
        visualization_b64 = ""
        print(" Visualization code generated")
        
        print(" Generation complete!")
        
        return StudyMaterial(
            notes=notes,
            quiz=quiz_items,
            merged_content=merged,
            visualization=visualization_b64,
            mermaid_code=mermaid_code,
        )
        
    except Exception as e:
        print(f"Error during generation: {str(e)}")
        error_detail = str(e)
        
        # Provide more helpful error messages
        if "Connection refused" in error_detail:
            error_detail = "Could not connect to Ollama. Please make sure Ollama is running and the model is available."
        elif "timeout" in error_detail.lower():
            error_detail = "Request timed out. The LLM took too long to respond. Please try again with a shorter text."
        elif "memory" in error_detail.lower() or "gpu" in error_detail.lower():
            error_detail = "GPU/Memory error. Try using a smaller model or shorter text."
        elif "model" in error_detail.lower() and "not found" in error_detail.lower():
            error_detail = "Model not found. Please ensure the required model is downloaded in Ollama."
        
        raise HTTPException(status_code=500, detail=error_detail)

@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "AI Study Assistant is running!"}

if __name__ == "__main__":
    import uvicorn
    
    # Get port from environment or use default
    port = int(os.getenv("PORT", 8000))
    host = os.getenv("HOST", "0.0.0.0")
    
    print(f"\n🚀 Starting AI Study Assistant on {host}:{port}")
    print(f"📝 Access at: http://localhost:{port}")
    print(f"🌐 For ngrok: ngrok http {port}\n")
    
    uvicorn.run("backend:app", host=host, port=port, reload=True)