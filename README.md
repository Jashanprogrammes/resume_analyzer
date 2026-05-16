# 🤖 AI Resume Analyzer — Python Project

A full-stack web app that analyzes resumes using GROQ API and gives instant feedback.

## Setup (2 minutes)

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Set your API key
Get a free API key from Groq's console

**Windows:**
```bash
set GROQ_API_KEY=your_key_here
```
**Mac/Linux:**
```bash
export GROQ_API_KEY=your_key_here
```

### 3. Run the app
```bash
python app.py
```

Open **http://localhost:5000** in your browser. Done! ✅

---

## Project Structure
```
resume_analyzer/
├── app.py              ← Flask backend + AI logic
├── requirements.txt    ← Dependencies
└── templates/
    └── index.html      ← Frontend UI
```

## Features
- 📄 Upload any PDF resume
- 🎯 Target a specific job role
- 📊 Overall score (0–100) with animated ring
- ✅ Strengths, weaknesses, suggestions
- 🔑 Keywords extracted
- 📈 ATS compatibility score
- 💡 Missing sections detection
