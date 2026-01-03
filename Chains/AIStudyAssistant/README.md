# 🎓 AI Study Assistant - Complete Setup Guide

A beautiful full-stack application that generates study notes, interactive quizzes, and visualizes LangChain execution flows with professional animations.

## ✨ Features

- 📝 **AI-Powered Notes Generation** - Converts any topic into concise, formatted study notes
- 🎯 **Interactive Quiz** - Generates 5 questions with 4 options each, with instant feedback
- 🔄 **Chain Visualization** - Beautiful animated flow showing how LangChain processes your request
- 📋 **Copy Notes** - Export notes as Markdown or Plain Text
- 💾 **Download Visualization** - Save your chain diagrams as PNG
- 🌐 **Network Sharing** - Easy setup with ngrok for sharing your app
- 🤖 **Local Ollama Support** - Use local models for privacy and speed

## 📁 Project Structure

```
AI-Study-Assistant/
├── backend.py              # FastAPI backend server
├── static/                 # Frontend files
│   ├── index.html         # Main UI
│   ├── script.js          # Frontend logic
│   └── styles.css         # Beautiful styling
├── .env                   # Environment variables (create from .env.example)
├── .env.example          # Template for environment variables
├── requirements.txt      # Python dependencies
└── README.md            # This file
```

## 🚀 Installation

### Prerequisites

1. **Python 3.10+** installed
2. **Ollama** installed and running (for local models)
   - Download from: https://ollama.ai
   - Install model: `ollama pull llama3.2:3b`
3. **(Optional)** HuggingFace API token for cloud models

### Step 1: Clone or Create Project Structure

Create the following folder structure:
```bash
mkdir AI-Study-Assistant
cd AI-Study-Assistant
mkdir static
```

### Step 2: Add Files

Place all the files in their correct locations:
- `backend.py` in the root directory
- `index.html`, `script.js`, `styles.css` in the `static/` folder
- `.env.example` and `requirements.txt` in the root directory

### Step 3: Install Dependencies

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Step 4: Configure Environment

```bash
# Copy .env.example to .env
cp .env.example .env

# Edit .env and add your tokens (optional for HuggingFace)
# If using only Ollama, you don't need to change anything
```

### Step 5: Start Ollama (if using local models)

```bash
# Make sure Ollama is running
ollama serve

# Pull the model (if not already done)
ollama pull llama3.2:3b
```

## 🎮 Running the Application

### Standard Local Run

```bash
# Make sure you're in the project directory and virtual environment is activated
python backend.py
```

The app will be available at: `http://localhost:8000`

### Using Custom Port

```bash
# Set custom port in .env
PORT=5000

# Or run with environment variable
PORT=5000 python backend.py
```

## 🌐 Network Sharing with Ngrok

### Option 1: Using Ngrok

1. **Install Ngrok**
   ```bash
   # Download from: https://ngrok.com/download
   # Or install via package manager
   
   # Windows (Chocolatey):
   choco install ngrok
   
   # Mac:
   brew install ngrok
   ```

2. **Setup Ngrok Auth**
   ```bash
   # Get your auth token from: https://dashboard.ngrok.com/get-started/your-authtoken
   ngrok config add-authtoken YOUR_TOKEN_HERE
   ```

3. **Start Your Backend**
   ```bash
   python backend.py
   ```

4. **In a New Terminal, Start Ngrok**
   ```bash
   ngrok http 8000
   ```

5. **Share the URL**
   - Ngrok will show a forwarding URL like: `https://abc123.ngrok.io`
   - Share this URL with anyone to access your app!

### Option 2: Using Localtunnel

```bash
# Install localtunnel
npm install -g localtunnel

# Start your backend
python backend.py

# In a new terminal, expose it
lt --port 8000
```

### Option 3: Using VS Code Port Forwarding

1. Start your backend
2. In VS Code, go to **Ports** panel
3. Click **Forward a Port**
4. Enter `8000`
5. Right-click the port and set visibility to **Public**
6. Share the generated URL

## 📖 Usage Guide

### 1. Enter Your Topic
- Paste any long text or topic into the input area
- Can be articles, lecture notes, documentation, etc.

### 2. Generate Study Material
- Click "Generate Study Material"
- Check "Use Local Ollama" for faster, private processing
- Uncheck to use HuggingFace cloud models

### 3. Review Notes
- View formatted, concise notes
- Copy as Markdown or Plain Text for your notes app

### 4. Take the Quiz
- Answer all 5 multiple-choice questions
- Click "Check Answers" to see results
- Get instant feedback with correct answers

### 5. Explore Visualization
- Click "Play Animation" to see chain execution flow
- Watch how your input flows through parallel processing
- Download the visualization as PNG

### 6. Add More Topics
- Click "Add Another Topic" to study more content
- All previous content is preserved in the session

## 🎨 Customization

### Change Models

Edit `backend.py`:
```python
# For local Ollama
model1 = ChatOllama(model="llama3.2:3b", temperature=0.5)

# Try other models:
# - llama3.2:1b (faster, less accurate)
# - mistral:latest
# - codellama:latest
```

### Change Port

In `.env`:
```
PORT=5000  # or any port you want
```

### Modify Styling

Edit `static/styles.css` to change colors, animations, layout, etc.

## 🔧 Troubleshooting

### Ollama Connection Issues
```bash
# Check if Ollama is running
curl http://localhost:11434

# Start Ollama
ollama serve

# Check available models
ollama list
```

### Port Already in Use
```bash
# Kill process on port 8000 (Windows)
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Mac/Linux
lsof -ti:8000 | xargs kill -9
```

### Module Not Found Errors
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### CORS Issues
- Already configured in `backend.py`
- If issues persist, check browser console for specific errors

## 🚀 Production Deployment

### Using Gunicorn (Linux/Mac)
```bash
pip install gunicorn
gunicorn -w 4 -k uvicorn.workers.UvicornWorker backend:app --bind 0.0.0.0:8000
```

### Using Docker
Create `Dockerfile`:
```dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "backend.py"]
```

Build and run:
```bash
docker build -t ai-study-assistant .
docker run -p 8000:8000 ai-study-assistant
```

## 📝 API Endpoints

- `GET /` - Serves the web interface
- `POST /generate` - Generates study material
  ```json
  {
    "text": "Your topic text here",
    "use_local_ollama": true
  }
  ```
- `GET /health` - Health check endpoint

## 🤝 Contributing

Feel free to:
- Add more AI models
- Improve quiz generation logic
- Enhance visualizations
- Add export formats (PDF, DOCX)
- Implement user authentication
- Add study history tracking

## 📄 License

MIT License - feel free to use this for your projects!

## 🙏 Acknowledgments

- LangChain for the awesome framework
- Ollama for local AI models
- FastAPI for the backend
- FontAwesome for icons

---

**Made with ❤️ for students and learners everywhere!**

For issues or questions, feel free to reach out or open an issue on GitHub.

Happy Learning! 🎓✨