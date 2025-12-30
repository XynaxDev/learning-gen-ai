from langchain_ollama import ChatOllama
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import load_prompt 
import streamlit as st

st.header("Research Paper Summary Generator")
llm = ChatOllama(model="llama3.1:8b", temperature=0.5,max_tokens=500)
# ggl = ChatGoogleGenerativeAI(model="gemini-3-flash-preview", temperature=0.5, max_output_tokens=500)

template = load_prompt("prompts/research_paper_summary_prompt.json")

paper_title = st.text_input("Enter the title of the research paper:")
explanation_style = st.text_input("Enter the explanation style (e.g., simple, detailed, technical):")
explanation_length = st.text_input("Enter the explanation length (e.g., short, medium, long):")

btn = st.button("Generate Summary")

prompt = template.invoke({
        "paper_title": paper_title, 
        "explanation_style": explanation_style,
        "explanation_length": explanation_length
})

if btn:
    response = llm.invoke(prompt)
    st.subheader("Generated Summary:")
    st.write(response.content)
    # st.write(response.content[0]["text"])
    # For Ollama, use response.content directly
    # For Google Generative AI, use response.content[0]["text"]
