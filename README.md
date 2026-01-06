<div style="display:flex; align-items:center; gap:16px;">

<img src="./assets/logo.png" alt="Gen AI Journal Logo" height="200" width="200" style="border-radius:12px;" />
<div>

### `Gen AI Journal 📝` 
[Notion Journal](https://akgenai-journal.notion.site/Generative-AI-Journal-29fc4f0bd1aa8063819ecec314d0ae67?source=copy_link) | [Linkedin](https://linkedin.com/in/akass7) | [Gmail](mailto:akashkumar.cs27@gmail.com) | [Instagram](https://instagram.com/xynaxhere)


![Gen AI Journal](https://img.shields.io/badge/GenAI-Journal-8A2BE2?style=rounded&logo=openai&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=rounded&logo=python&logoColor=white)
![LangChain](https://img.shields.io/badge/LangChain-Ecosystem-0F9D58?style=rounded&logo=langchain&logoColor=white)
![Ollama](https://img.shields.io/badge/Ollama-LocalModels-00A86B?style=rounded&logo=ollama&labelColor=0A0A0A)
![OpenAI](https://img.shields.io/badge/OpenAI-APIs-000000?style=rounded&logo=openai&logoColor=white)
![Local + API Models](https://img.shields.io/badge/huggingface-Local_%2B_API-FF5722?style=rounded&logo=huggingface&logoColor=white)
![Mermaid](https://img.shields.io/badge/Mermaid-Diagrams-8B5CF6?style=rounded&logo=mermaid&logoColor=white)
![GitHub](https://img.shields.io/badge/GitHub-Repo-24292F?style=rounded&logo=github&logoColor=white)
![Notion](https://img.shields.io/badge/Notion-Journal-111111?style=rounded&logo=notion&logoColor=white)


</div>
</div>

---

### `About`

This repository is my living Generative AI lab and learning journal. It is organized around five core building blocks of modern GenAI systems: **`Models`**, **`Prompts`**, **`Chains`**, **`Indexes (RAG)`**, and **`Agents`**. Everything else in this repo exists to support, explore, or extend these core pieces.

Here I continuously add small, focused, and practical experiments:
- **`Models`** → local (Ollama) and hosted APIs, embeddings, and chat models 
- **`Prompts`** → prompt engineering techniques, templates, and structured prompting 
- **`Chains`** → sequential, parallel, conditional flows, routing, and orchestration logic 
- **`Indexes (RAG)`** → document loaders, chunking strategies, vector stores, retrieval pipelines 
- **`Agents`** → tool-using, multi-step reasoning, and decision-making workflows 

**The goal is simple:** **`learn by building`**. Every folder is a hands-on experiment, every script is a learning checkpoint. This is not a framework — it’s a **code-first playground** where I explore how real GenAI systems are composed, connected, and scaled.

> ⚙️ Built with **Python** and the **LangChain ecosystem**, this journal documents my journey from basic LLM usage to composing full, production-style AI pipelines. 

### `Environment & setup`

- **Create virtual environment (optional but recommended)**

```bash
python -m venv venv
venv\Scripts\activate
```
- **Install Python dependencies**

```bash
pip install -r requirements.txt
```

- **Environment variables**
    - Copy `Models/.env.example` to `Models/.env` and fill in any required  API keys (e.g. OpenAI or other providers) when using API models.
    - Use the `Prompts/.env` file for any prompt-related secrets (chat history storage, API keys, etc.).


### `Local models (Ollama, custom LLMs)`
This project uses local models via Ollama, for example in `customLLm.py` with `ChatOllama` (e.g. `llama3.2:3b`).

- **Install and run Ollama**
    - Download and install from https://ollama.com
    - Start the Ollama service.
    - Pull a model (example):

```bash
ollama pull llama3.2:3b
```

- **Run a local LLM example**
```bash
python customLLm.py
```

### `API models (hosted providers)`
For scripts that use hosted APIs (e.g. OpenAI-style models) inside the `Models` and `Prompts` areas:
- **Set your API keys** inside `Models/.env` (and `Prompts/.env` if needed).
- Make sure the required client libraries are installed via `requirements.txt`.
- Run the example scripts directly with `python path/to/script.py`.

### `Chains`
Experiments around LangChain `Chain` primitives: simple, sequential, parallel, conditional flows, plus an AI study assistant.

- **What this area is for**
    - Exploring different chain patterns (simple, sequential, parallel, conditional).
    - Routing logic and basic decision flows inside chains.
    - The `AIStudyAssistant` subfolder holds a more applied study-helper example.

- **Explore code**
- [./Chains/](./Chains/)

### `IndexesRAG*` 
Working with document loaders and text splitters to build retrieval-augmented generation (RAG) style pipelines.

- **What this area is for**
    - Trying different `DocumentLoaders` to bring data into the system.
    - Experimenting with `TextSplitters` for chunking text before indexing.
    - Forming the basis for retrieval and semantic search workflows.

- **Explore code**
- [./IndexesRAG/](./IndexesRAG/)

### `Models`
Central place for LLMs, chat models, embedding models, and semantic search utilities.

- **What this area is for**
    - `ChatModels/`: chat-style conversational models.
    - `EmbeddingModels/`: vector embeddings for similarity and search.
    - `LLMs/`: generic LLM examples and utilities.
    - Semantic search and retrieval experiments.

- **Explore code**
- [./Models/](./Models/)

### `Prompts`
Prompt-focused experiments and chat-oriented utilities.

- **What this area is for**
    - `PromptTechniques/`: different prompt patterns and techniques.
    - `ChatBot/`: chatbot flows and interactions.
    - Working with static vs dynamic prompts and prompt generators.
    - Building structured chat prompts, message templates, and chat history handling.

- **Explore code**
- [./Prompts/](./Prompts/)

### `Runnables`
Using LangChain `Runnable*` primitives to compose more advanced and flexible workflows.

- **What this area is for**
    - `runnableSequence.py`: chaining steps in sequence.
    - `runnableParallel.py`: parallel branches that run at the same time.
    - `runnableBranch.py`: conditional branching logic.
    - `runnableLambda.py`, `runnablePassThrough.py`: functional / utility runnables.
    - `runnables_core.ipynb`: an interactive notebook exploring runnable concepts.

- **Explore code**
- [./Runnables/](./Runnables/)

### `StructuredOutputs`
Controlling and validating model outputs to match structured schemas.
- **What this area is for**
    - `BuiltinLLMs/`: structured-output features that are built into certain LLM providers.
    - `OutputParsers/`: parsing raw model text into JSON or typed Python objects.
- **Explore code**
- [./StructuredOutputs/](./StructuredOutputs/)
  
### `Useful Resources & Explorers` 
These are some genuinely great tools and references I often use while experimenting:

- 🔍 **Chunk Visualizer**
    - https://huggingface.co/spaces/m-ric/chunk_visualizer 
    - https://chunkviz.up.railway.app/

- 📄 **LangChain Document Loaders**
    - https://docs.langchain.com/oss/python/integrations/document_loaders

- 🏆 **Open LLM Leaderboard**
    - https://huggingface.co/spaces/open-llm-leaderboard/open_llm_leaderboard

- 🧠 **LangChain Python Docs**
    - https://python.langchain.com/docs/

- 🤗 **HuggingFace Models Hub**
    - https://huggingface.co/models

- 🧩 **Pydantic Docs (for structured outputs)**
    - https://docs.pydantic.dev/

- 🦙 **Ollama**
    - https://ollama.com

### `Thank you for reading` 💌

This repo is not a “`perfect framework`” — it’s a **learning log, playground, and experiment tracker**. 
If you’re also learning **GenAI**, feel free to explore, fork, break things, improve them, and build your own versions.
> If something here helps you, that’s already a win. If you have ideas or improvements **even better**. 
> Let’s keep learning and shipping 🚢✨🫱🏼‍🫲🏼