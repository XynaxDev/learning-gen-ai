from langchain_text_splitters import RecursiveCharacterTextSplitter, Language

text = """
## 📁 Project Layout
- `project_settings/settings.py` — Environment-driven configuration (email, hosts, security).  
- `core/`, `api/`, `accounts/`, `ml/` — Main Django apps.  
- `static/` → Collected to `staticfiles/` for production use.  
- `.env.example` — Template to create your `.env` file safely.  
- `.gitignore` — Excludes sensitive data, caches, sessions, media, and logs.

---

## ⚡ Quick Start (Local)
1. **Create a virtual environment and install dependencies**:  
    ```bash
    pip install -r requirements.txt
    ```
2. **Copy environment template and configure**:  
    ```bash
    cp .env.example .env
    ```
3. **Collect static files and run the server**:  
    ```bash
    python manage.py collectstatic --noinput
    python manage.py runserver
    ```
4. Open [http://127.0.0.1:8000](http://127.0.0.1:8000) in your browser.
"""

splitter = RecursiveCharacterTextSplitter.from_language(
    language=Language.MARKDOWN,
    chunk_size= 500,
    chunk_overlap=0
)

chunks = splitter.split_text(text)
print(len(chunks))
print(chunks)