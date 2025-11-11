# 💻 AI Coding Assistant

**Your Local, Private Coding Companion**

A comprehensive AI-powered coding assistant that runs 100% locally or with cloud AI models. Built with Python, Streamlit, LangChain, and SQLite, featuring 10 specialized tools for code generation, debugging, quality analysis, and more.

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Technology Stack](#technology-stack)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage Guide](#usage-guide)
- [Data Flow](#data-flow)
- [Project Structure](#project-structure)
- [Implementation Details](#implementation-details)
- [Privacy & Security](#privacy--security)
- [Contributing](#contributing)

---

## 🎯 Overview

The AI Coding Assistant is a multi-functional development tool that provides intelligent code assistance through a clean, intuitive interface. It supports both local AI models (Llama 3.1 via Ollama) and cloud models (Google Gemini 2.0 Flash), giving users flexibility between privacy and performance.

### Key Highlights

- **10 Specialized Tools**: Each designed for specific coding tasks
- **Dual AI Support**: Toggle between local Llama 3.1 and cloud Gemini 2.0
- **Privacy-First**: All data stored locally in SQLite
- **Semantic Search**: FAISS-powered search through conversation history
- **Multi-Language**: Supports 14+ programming languages
- **Code Playground**: Test code directly in the browser

---

## ✨ Features

### 1. 💬 Chat Assistant
- **Purpose**: General coding conversations with context awareness
- **Capabilities**:
  - Multi-turn conversations with memory
  - Context-aware responses using conversation history
  - Semantic search integration for relevant past discussions
  - Export conversations as markdown
- **Use Cases**: Ask questions, discuss best practices, get coding advice

### 2. 🔧 Code Generator
- **Purpose**: Generate production-ready code from natural language descriptions
- **Capabilities**:
  - Support for 12+ programming languages
  - Optional unit test generation
  - Documentation inclusion
  - Usage examples
- **Use Cases**: Rapid prototyping, boilerplate generation, algorithm implementation

### 3. 🐛 Bug Fixer
- **Purpose**: Automated debugging and code repair
- **Capabilities**:
  - Side-by-side code comparison (original vs fixed)
  - Detailed bug analysis report with severity levels
  - Error message interpretation
  - Explanation of fixes applied
  - Downloadable bug reports
- **Use Cases**: Debug syntax errors, fix logic issues, resolve runtime problems

### 4. 📊 Code Quality Analyzer
- **Purpose**: Comprehensive code review and quality assessment
- **Capabilities**:
  - Performance analysis
  - Security vulnerability detection
  - Style and best practices review
  - Severity-based issue categorization (Critical/High/Medium/Low)
  - Actionable recommendations
- **Use Cases**: Pre-commit reviews, code audits, learning best practices

### 5. ♻️ Code Refactoring
- **Purpose**: Improve code structure and maintainability
- **Capabilities**:
  - Multiple refactoring goals (readability, performance, complexity reduction)
  - Design pattern application
  - Type hint/annotation addition
  - Behavior preservation option
  - Before/after comparison
- **Use Cases**: Technical debt reduction, code modernization, optimization

### 6. 📝 Documentation Generator
- **Purpose**: Auto-generate comprehensive code documentation
- **Capabilities**:
  - Multiple documentation styles (inline, docstrings, README, API docs)
  - Usage examples inclusion
  - Multi-language support
  - Markdown export
- **Use Cases**: API documentation, code comments, README generation

### 7. 🧪 Test Generator
- **Purpose**: Create comprehensive unit tests
- **Capabilities**:
  - Multiple test frameworks (pytest, Jest, JUnit, etc.)
  - Configurable coverage goals (50-100%)
  - Edge case testing
  - Mock/stub generation
- **Use Cases**: TDD, test coverage improvement, regression testing

### 8. 🔍 Code Explainer
- **Purpose**: Understand complex code at any skill level
- **Capabilities**:
  - Three detail levels (Beginner, Intermediate, Advanced)
  - Structured explanations (overview, breakdown, concepts)
  - Focus areas (algorithms, data structures, patterns)
  - Side-by-side code and explanation
- **Use Cases**: Learning, code reviews, onboarding

### 9. ⚡ Code Playground
- **Purpose**: Test and run code instantly in the browser
- **Capabilities**:
  - Python execution (built-in)
  - JavaScript execution (requires Node.js)
  - Syntax highlighting for 6+ languages
  - Example code templates
  - 5-second execution timeout for safety
- **Use Cases**: Quick testing, prototyping, learning

### 10. 📚 History
- **Purpose**: Search and manage conversation history
- **Capabilities**:
  - Keyword search across all conversations
  - Semantic search using FAISS embeddings
  - View recent conversations
  - Rebuild search index
- **Use Cases**: Reference past solutions, track progress, reuse code

---

## 🏗️ Architecture

### System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Streamlit Frontend                       │
│  (Home.py + 10 Page Modules)                                │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                  Core Components                             │
├─────────────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │ LLM Handler  │  │  Database    │  │  Embeddings  │     │
│  │              │  │              │  │              │     │
│  │ - Ollama     │  │ - SQLite     │  │ - FAISS      │     │
│  │ - Gemini API │  │ - History    │  │ - Sentence   │     │
│  │              │  │   Storage    │  │   Transform  │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
└─────────────────────────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                  External Services                           │
├─────────────────────────────────────────────────────────────┤
│  ┌──────────────┐              ┌──────────────┐            │
│  │   Ollama     │              │ Google Gemini│            │
│  │ (Local LLM)  │              │  (Cloud API) │            │
│  └──────────────┘              └──────────────┘            │
└─────────────────────────────────────────────────────────────┘
```

### Component Interaction

1. **User Interface Layer** (Streamlit)
   - Handles user input and displays results
   - Manages session state and navigation
   - Renders UI components and styling

2. **Business Logic Layer**
   - `llm_handler.py`: AI model abstraction and prompt management
   - `sidebar_config.py`: Global sidebar configuration
   - Page modules: Feature-specific logic

3. **Data Layer**
   - `database.py`: SQLite operations for conversation storage
   - `embeddings.py`: FAISS vector search for semantic retrieval
   - `history.db`: Persistent storage file

---

## 🛠️ Technology Stack

### Frontend
- **Streamlit 1.28+**: Web application framework
- **Custom CSS**: Dark theme and responsive design

### Backend
- **Python 3.8+**: Core programming language
- **LangChain**: LLM orchestration and prompt management
- **LangChain Community**: Ollama integration

### AI Models
- **Ollama**: Local LLM runtime
  - Model: Llama 3.1 (4.9 GB)
  - Fully offline operation
- **Google Gemini 2.0 Flash**: Cloud AI
  - API-based access
  - Faster responses

### Data Storage
- **SQLite3**: Conversation history database
- **FAISS**: Vector similarity search
- **Sentence Transformers**: Text embeddings (all-MiniLM-L6-v2)

### Additional Libraries
- **python-dotenv**: Environment variable management
- **subprocess**: Code execution in playground
- **tempfile**: Temporary file handling

---

## 📦 Installation

### Prerequisites

1. **Python 3.8 or higher**
   ```bash
   python --version
   ```

2. **Ollama** (for local AI)
   - Download from: https://ollama.ai
   - Install Llama 3.1 model:
   ```bash
   ollama pull llama3.1:latest
   ```

3. **Node.js** (optional, for JavaScript playground)
   - Download from: https://nodejs.org

### Setup Steps

1. **Clone or download the project**
   ```bash
   cd CodingAssistant
   ```

2. **Create virtual environment** (recommended)
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # Linux/Mac
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   ```bash
   # Copy example file
   cp .env.example .env
   
   # Edit .env and add your Gemini API key (optional)
   GEMINI_API_KEY=your_api_key_here
   ```

5. **Run the application**
   ```bash
   streamlit run Home.py
   ```

6. **Access the app**
   - Open browser to: http://localhost:8501

---

## ⚙️ Configuration

### Environment Variables (.env)

```env
# Google Gemini API Key (optional)
GEMINI_API_KEY=your_gemini_api_key_here
```

### Streamlit Configuration (.streamlit/config.toml)

```toml
[ui]
hideTopBar = false

[runner]
fastReruns = true

[client]
showErrorDetails = true
toolbarMode = "minimal"

[server]
headless = false

[browser]
gatherUsageStats = false

[theme]
base = "dark"
```

### Model Selection

Toggle between AI models in the sidebar:
- **Gemini 2.0 Flash**: Faster, requires API key, cloud-based
- **Llama 3.1**: Private, slower, fully local

---

## 📖 Usage Guide

### Getting Started

1. **Launch the application**
   ```bash
   streamlit run Home.py
   ```

2. **Select AI Model**
   - Use the toggle in the sidebar
   - Default: Gemini 2.0 Flash (if API key configured)
   - Alternative: Llama 3.1 (local)

3. **Choose a Tool**
   - Click on any feature card on the home page
   - Or use the sidebar navigation

### Example Workflows

#### Workflow 1: Generate and Test Code

1. Go to **Code Generator**
2. Describe your function: "Create a Python function to validate email addresses"
3. Select language: Python
4. Enable "Include unit tests"
5. Click "Generate Code"
6. Copy the generated code
7. Go to **Code Playground**
8. Paste and test the code
9. If issues found, go to **Bug Fixer**

#### Workflow 2: Improve Existing Code

1. Go to **Code Quality Analyzer**
2. Paste your code
3. Select checks: Performance, Security, Style
4. Review the analysis
5. Go to **Refactor**
6. Paste the same code
7. Select refactoring goals
8. Compare before/after
9. Go to **Documentation**
10. Generate docs for the refactored code

#### Workflow 3: Learn from Code

1. Find complex code you want to understand
2. Go to **Code Explainer**
3. Paste the code
4. Select detail level (Beginner/Intermediate/Advanced)
5. Read the structured explanation
6. Go to **Chat** for follow-up questions

---

## 🔄 Data Flow

### Request Flow

```
User Input
    │
    ▼
Streamlit Page
    │
    ├─→ Session State (model selection, API key)
    │
    ▼
LLM Handler
    │
    ├─→ [If Gemini] → Google API → Response
    │
    └─→ [If Llama] → Ollama → Local Model → Response
    │
    ▼
Response Processing
    │
    ├─→ Display to User
    │
    └─→ Save to Database
         │
         ▼
    SQLite (history.db)
         │
         └─→ Generate Embeddings → FAISS Index
```

### Data Storage

1. **Conversation Storage**
   ```sql
   CREATE TABLE conversations (
       id INTEGER PRIMARY KEY AUTOINCREMENT,
       timestamp TEXT NOT NULL,
       user_query TEXT NOT NULL,
       ai_response TEXT NOT NULL,
       code_snippet TEXT,
       language TEXT
   );
   ```

2. **Embedding Generation**
   - Text → Sentence Transformer → 384-dim vector
   - Vector → FAISS Index → Fast similarity search

3. **Search Process**
   - Query → Embedding → FAISS Search → Top K results
   - Results → Context → Enhanced LLM prompt

---

## 📁 Project Structure

```
CodingAssistant/
├── Home.py                      # Main entry point (home page)
├── sidebar_config.py            # Global sidebar configuration
├── llm_handler.py              # AI model abstraction layer
├── database.py                 # SQLite operations
├── embeddings.py               # FAISS semantic search
├── style.css                   # Custom CSS styling
├── requirements.txt            # Python dependencies
├── .env                        # Environment variables (not in git)
├── .env.example               # Environment template
├── .gitignore                 # Git ignore rules
├── README.md                  # This file
│
├── .streamlit/
│   └── config.toml            # Streamlit configuration
│
├── pages/                     # Feature modules
│   ├── 1_💬_Chat.py
│   ├── 2_🔧_Code_Generator.py
│   ├── 3_🐛_Bug_Fixer.py
│   ├── 4_📊_Code_Quality.py
│   ├── 5_♻️_Refactor.py
│   ├── 6_📝_Documentation.py
│   ├── 7_🧪_Test_Generator.py
│   ├── 8_🔍_Code_Explainer.py
│   ├── 9_📚_History.py
│   └── 10_⚡_Code_Playground.py
│
└── history.db                 # SQLite database (auto-generated)
```

---

## 🔧 Implementation Details

### LLM Handler (`llm_handler.py`)

**Purpose**: Abstraction layer for AI models

**Key Methods**:
- `__init__()`: Initialize model (Ollama or Gemini)
- `generate_response()`: General chat responses
- `generate_code()`: Code generation
- `fix_bug()`: Bug fixing
- `analyze_quality()`: Code quality analysis
- `refactor_code()`: Code refactoring
- `generate_docs()`: Documentation generation
- `generate_tests()`: Test generation
- `explain_code()`: Code explanation

**Model Switching Logic**:
```python
if use_gemini and api_key:
    # Initialize Gemini
    import google.generativeai as genai
    genai.configure(api_key=api_key)
    self.llm = genai.GenerativeModel('gemini-2.0-flash-exp')
else:
    # Initialize Ollama
    self.llm = Ollama(model="llama3.1:latest")
```

### Database Handler (`database.py`)

**Purpose**: Manage conversation persistence

**Schema**:
- `id`: Auto-incrementing primary key
- `timestamp`: ISO format datetime
- `user_query`: User's input
- `ai_response`: AI's response
- `code_snippet`: Extracted code (optional)
- `language`: Programming language (optional)

**Key Methods**:
- `add_conversation()`: Store new conversation
- `get_all_conversations()`: Retrieve all history
- `search_by_keyword()`: Keyword-based search

### Embeddings Handler (`embeddings.py`)

**Purpose**: Semantic search using FAISS

**Process**:
1. Load sentence transformer model (all-MiniLM-L6-v2)
2. Generate embeddings for all conversations
3. Build FAISS index (L2 distance)
4. Search: Query → Embedding → FAISS → Top K results

**Key Methods**:
- `build_index()`: Create FAISS index from conversations
- `search()`: Find similar conversations

### Sidebar Configuration (`sidebar_config.py`)

**Purpose**: Global sidebar across all pages

**Features**:
- Model toggle (Gemini/Llama)
- Session state initialization
- Consistent branding

### Page Modules

Each page follows this structure:
1. Set page config
2. Initialize components (DB, LLM)
3. Load custom CSS
4. Render sidebar
5. Display page-specific UI
6. Handle user interactions
7. Process with LLM
8. Display results
9. Save to database

---

## 🔒 Privacy & Security

### Data Privacy

1. **Local Storage**
   - All conversations stored in local SQLite database
   - No external data transmission (except when using Gemini)
   - Database file: `history.db` (in project root)

2. **API Key Security**
   - Stored in `.env` file (git-ignored)
   - Never logged or displayed
   - Only used for API authentication

3. **Code Execution**
   - Playground runs in isolated subprocess
   - 5-second timeout limit
   - No file system access
   - No network access

### Security Best Practices

1. **Never commit `.env` file**
2. **Use virtual environment**
3. **Keep dependencies updated**
4. **Review generated code before execution**
5. **Use local model for sensitive code**

---

## 🌐 Supported Languages

- Python
- JavaScript
- TypeScript
- Java
- C++
- Go
- Rust
- C#
- PHP
- Ruby
- Swift
- Kotlin
- SQL
- Bash

---

## 🚀 Performance

### Response Times (Approximate)

| Model | Simple Query | Code Generation | Complex Analysis |
|-------|-------------|-----------------|------------------|
| Gemini 2.0 | 1-2s | 3-5s | 5-10s |
| Llama 3.1 | 5-10s | 15-30s | 30-60s |

### Resource Usage

- **Memory**: 500MB - 2GB (depending on model)
- **Disk**: ~100MB (app) + 4.9GB (Llama model)
- **CPU**: Moderate (Gemini) / High (Llama)

---

## 🐛 Troubleshooting

### Common Issues

1. **"Ollama not found"**
   - Install Ollama from https://ollama.ai
   - Run: `ollama pull llama3.1:latest`

2. **"Gemini API error"**
   - Check API key in `.env`
   - Verify key at https://aistudio.google.com/apikey
   - Check internet connection

3. **"Database locked"**
   - Close other instances of the app
   - Delete `history.db` and restart

4. **"Module not found"**
   - Reinstall dependencies: `pip install -r requirements.txt`

---

## 📝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

---

## 📄 License

This project is for educational and personal use.

---

## 🙏 Acknowledgments

- **Ollama**: Local LLM runtime
- **Google**: Gemini AI API
- **Streamlit**: Web framework
- **LangChain**: LLM orchestration
- **FAISS**: Vector similarity search

---

