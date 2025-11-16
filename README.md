# CodeSage - AI-Powered Code Understanding Platform

![CodeSage](https://img.shields.io/badge/CodeSage-AI%20Code%20Understanding-blue)
![Python](https://img.shields.io/badge/Python-3.11+-green)
![TypeScript](https://img.shields.io/badge/TypeScript-5.2+-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green)
![React](https://img.shields.io/badge/React-18.2+-blue)
![Docker](https://img.shields.io/badge/Docker-Ready-blue)
![Tests](https://img.shields.io/badge/Tests-Passing-green)

**CodeSage** is an innovative full-stack application that leverages Mistral AI to provide intelligent code analysis, documentation generation, and Q&A capabilities. Built with modern best practices, it uses the Strategy Pattern for extensible code analysis and integrates seamlessly with Mistral AI's API.

## 📚 Documentation

- **[README.md](./README.md)** - This file: Setup, usage, and overview

## 🎯 Features

- **Intelligent Code Analysis**: Upload code files and get comprehensive analysis including:

  - Language detection and parsing
  - Complexity scoring
  - Function and class extraction
  - Import analysis
  - Code quality metrics
- **AI-Powered Insights**: Enhanced analysis using Mistral AI for:

  - Code quality assessment with specific, actionable recommendations
  - Best practices recommendations with exact function/class names
  - Security concerns identification
  - Performance optimization suggestions
  - Maintainability improvements
- **Interactive Q&A**: Ask questions about your code and get intelligent answers powered by Mistral AI
- **Documentation Generation**: Automatically generate comprehensive documentation for your code files
- **Multi-Language Support**: Supports Python, JavaScript, TypeScript, Java, C++, Go, Rust, and many more
- **Modern UI**: Beautiful, responsive interface built with React, TypeScript, and Tailwind CSS with markdown rendering

## 🚀 Quick Start with Docker (Recommended)

The easiest way to run CodeSage is using Docker Compose - **just one command!**

### Prerequisites

- **Docker** 20.10+ and **Docker Compose** 2.0+ ([Install Docker](https://docs.docker.com/get-docker/))
- **Mistral AI API Key** ([Get one here](https://console.mistral.ai/))

### One-Command Setup

1. **Clone the repository**:

```bash
git clone <repository-url>
cd arkham
```

2. **Create `.env` file in the root directory**:

```bash
cp .env.example .env
```

3. **Edit `.env` and add your Mistral API key** (REQUIRED):

```env
MISTRAL_API_KEY=your_mistral_api_key_here
```

**Important**: Without a valid Mistral API key, the application will run but AI features (code analysis, Q&A, documentation generation) will be unavailable. Get your API key from [Mistral AI Console](https://console.mistral.ai/).

4. **Start everything with one command**:

```bash
docker compose up --build
```

That's it! The application will be available at:

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

The Docker setup automatically:

- Builds both frontend and backend containers
- Sets up networking between services
- Configures nginx to proxy API requests
- Handles health checks and auto-restart
- Mounts volumes for file uploads

### Docker Commands

```bash
# Start services
docker compose up

# Start in background
docker compose up -d

# Stop services
docker compose down

# View logs
docker compose logs -f

# Rebuild after changes
docker compose up --build

# Stop and remove volumes
docker compose down -v
```

## 🏗️ Architecture

### Backend (FastAPI + Python)

- **Strategy Pattern**: Extensible code analyzers for different programming languages
- **Service Layer**: Clean separation of concerns with dedicated services
- **Mistral AI Integration**: Seamless integration with Mistral AI API
- **RESTful API**: Well-structured endpoints for all features
- **Type Safety**: Pydantic models for validation

### Frontend (React + TypeScript + Tailwind)

- **Component-Based**: Modular, reusable React components
- **Type-Safe**: Full TypeScript implementation
- **Modern Styling**: Tailwind CSS for beautiful, responsive design
- **Markdown Rendering**: Beautiful markdown with syntax highlighting
- **User-Friendly**: Intuitive interface with drag-and-drop file uploads

## 📖 Usage Guide

### Getting Started

1. **Start the application** (see Quick Start above)
2. **Open your browser** to http://localhost:3000
3. **Upload a code file** to begin analysis

### 1. Analyze Code

**Step-by-step:**

1. Navigate to the **"Analyze Code"** tab
2. **Upload a file** using one of these methods:
   - Drag and drop a code file onto the upload area
   - Click the upload area to browse and select a file
   - Supported formats: `.py`, `.js`, `.ts`, `.tsx`, `.jsx`, `.java`, `.cpp`, `.go`, `.rs`, and many more
3. **Wait for analysis** (typically 5-15 seconds depending on file size)
4. **Review results**:
   - **Basic Analysis**: Language detection, complexity score, functions, classes, imports
   - **AI Insights**: Code quality assessment with overall score
   - **Recommendations**: Specific, actionable suggestions with:
     - Exact function/class names to modify
     - Before/after code examples
     - Implementation steps
     - Impact analysis

**Example Use Cases:**
- Review code quality before committing
- Get suggestions for refactoring
- Understand code structure and complexity
- Identify security concerns
- Find performance optimization opportunities

### 2. Ask Questions About Code

**Step-by-step:**

1. **First, analyze a code file** in the "Analyze Code" tab (this loads the code into context)
2. Navigate to the **"Ask Questions"** tab
3. The analyzed code is **automatically available** - you'll see a confirmation message
4. **Enter your question** in the text area, for example:
   - "What does this function do?"
   - "How can I optimize this code?"
   - "Explain the class structure"
   - "What are potential bugs here?"
5. **Select the programming language** (auto-detected from analysis)
6. Click **"Ask Question"**
7. **Get AI-powered answers** with markdown formatting, code examples, and explanations

**Tips:**
- Be specific in your questions for better answers
- Reference specific functions or classes by name
- Ask follow-up questions for deeper understanding

### 3. Generate Documentation

**Step-by-step:**

1. Navigate to the **"Generate Docs"** tab
2. **Option A**: If you've already analyzed a file:
   - Click **"Generate Documentation for Analyzed File"**
   - Uses the code from your previous analysis
3. **Option B**: Upload a new file:
   - Drag and drop or select a code file
   - Click **"Generate Documentation"**
4. **Wait for generation** (typically 10-30 seconds)
5. **Review the documentation**:
   - Overview and description
   - Function and class documentation
   - Usage examples
   - API references (if applicable)
6. **Download** the documentation as markdown

**Documentation includes:**
- Module/package overview
- Function signatures and docstrings
- Class hierarchies and methods
- Usage examples
- Best practices and notes

### Supported File Types

- **Python**: `.py`, `.pyw`
- **JavaScript**: `.js`, `.jsx`
- **TypeScript**: `.ts`, `.tsx`
- **Java**: `.java`
- **C/C++**: `.c`, `.cpp`, `.h`, `.hpp`
- **Go**: `.go`
- **Rust**: `.rs`
- **And many more**: `.rb`, `.php`, `.swift`, `.kt`, `.scala`, `.sql`, `.html`, `.css`, `.json`, `.yaml`, `.md`, `.txt`

**File Size Limit**: 10MB per file

## 🧪 Testing

CodeSage includes comprehensive test suites for both backend and frontend.

### Quick Test Commands

**Easiest Way - Use the Test Script:**
```bash
# Run all tests (automatically detects Docker or local)
./run-tests.sh

# Run specific test suites
./run-tests.sh backend
./run-tests.sh frontend

# Run with coverage
./run-tests.sh coverage

# Get help
./run-tests.sh help
```

**Manual Commands:**

**Backend Tests:**
```bash
# Using Docker
docker compose exec backend pytest tests/ -v

# Or locally
cd backend
pytest tests/ -v

# With coverage
pytest tests/ --cov=app --cov-report=html
```

**Frontend Tests:**
```bash
# Note: Frontend Docker container is production-only (nginx), so tests run locally
cd frontend
npm test

# With coverage
npm run test:coverage

# Watch mode (for development)
npm run test:watch
```

**Note**: The frontend Docker container uses nginx for production serving and doesn't include npm/node. Frontend tests should be run locally even when using Docker for the backend.

### Test Coverage

- **Backend**: Tests for services, strategies, and core functionality
- **Frontend**: Component tests and API type validation


## 📁 Project Structure

```
arkham/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   └── routes.py          # API endpoints
│   │   ├── core/
│   │   │   ├── config.py          # Configuration
│   │   │   ├── logging.py         # Logging setup
│   │   │   └── strategies/        # Strategy pattern implementation
│   │   │       ├── base.py        # Base analyzer interface
│   │   │       ├── python_analyzer.py
│   │   │       ├── javascript_analyzer.py
│   │   │       ├── typescript_analyzer.py
│   │   │       ├── generic_analyzer.py
│   │   │       └── strategy_factory.py
│   │   └── services/
│   │       ├── mistral_service.py  # Mistral AI integration
│   │       └── code_service.py     # Code analysis orchestration
│   ├── main.py                     # FastAPI application entry point
│   ├── requirements.txt            # Python dependencies
│   ├── Dockerfile                  # Backend Docker configuration
│   └── tests/                      # Backend tests
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── FileUpload.tsx
│   │   │   ├── CodeAnalysis.tsx
│   │   │   ├── CodeQuestion.tsx
│   │   │   ├── DocumentationGenerator.tsx
│   │   │   └── MarkdownRenderer.tsx
│   │   ├── services/
│   │   │   └── api.ts             # API client
│   │   ├── App.tsx                # Main application component
│   │   └── main.tsx               # Entry point
│   ├── package.json
│   ├── Dockerfile                  # Frontend Docker configuration
│   └── tests/                     # Frontend tests
│
├── docker-compose.yml              # Docker Compose configuration
├── .env.example                    # Environment variables template
└── README.md                       # This file
```

## 🎨 Design Patterns & Best Practices

### Strategy Pattern

The application uses the Strategy Pattern for code analysis, allowing easy extension to support new programming languages:

```python
# Each analyzer implements the CodeAnalyzerStrategy interface
class PythonAnalyzer(CodeAnalyzerStrategy):
    def can_analyze(self, file_extension: str) -> bool:
        return file_extension.lower() in ['.py', '.pyw']
  
    async def analyze(self, code_content: str, filename: str) -> AnalysisResult:
        # Python-specific analysis logic
        ...
```

### Service Layer Pattern

Clean separation of concerns with dedicated services:

- `MistralService`: Handles all Mistral AI interactions
- `CodeService`: Orchestrates code analysis workflow

### Type Safety

- Full TypeScript implementation in frontend
- Pydantic models for backend type validation
- Explicit return types throughout

### Error Handling

- Comprehensive error handling with meaningful messages
- Graceful degradation when AI services are unavailable

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the root directory (copy from `.env.example`):

```env
# Required - Get your API key from https://console.mistral.ai/
MISTRAL_API_KEY=your_mistral_api_key_here

# Optional - Backend Configuration (defaults shown)
API_HOST=0.0.0.0
API_PORT=8000

# Optional - CORS Configuration (comma-separated)
CORS_ORIGINS=http://localhost:3000,http://localhost:5173

# Optional - File Upload Configuration
MAX_FILE_SIZE=10485760  # 10MB in bytes
UPLOAD_DIR=./uploads
TEMP_DIR=./temp
```

**Important Notes:**
- The `.env` file works for both Docker and non-Docker setups when placed in the root directory
- The backend automatically searches for `.env` in both `backend/` and root directories
- Never commit your `.env` file to version control (it's in `.gitignore`)
- Use `.env.example` as a template for required variables

### Docker Configuration

The `docker-compose.yml` file handles:

- Backend service on port 8000
- Frontend service on port 3000
- Automatic health checks
- Volume mounting for uploads
- Network configuration for service communication

## 📊 API Endpoints

### POST `/api/v1/analyze`

Analyze uploaded code file

- **Request**: Multipart form data with `file`
- **Response**: Complete analysis results with AI insights

### POST `/api/v1/question`

Ask questions about code

- **Request**: Form data with `question`, `code_content`, `language`
- **Response**: AI-generated answer with markdown formatting

### POST `/api/v1/documentation`

Generate documentation

- **Request**: Multipart form data with `file`
- **Response**: Generated documentation in markdown format

### GET `/api/v1/supported-extensions`

Get list of supported file extensions

### GET `/health`

Health check endpoint

## 🛠️ Technologies Used

### Backend

- **FastAPI**: Modern, fast web framework
- **Mistral AI SDK**: AI-powered code analysis
- **Pydantic**: Data validation and settings management
- **Python AST**: For Python code parsing
- **aiofiles**: Async file operations
- **Uvicorn**: ASGI server

### Frontend

- **React 18**: UI library
- **TypeScript**: Type-safe JavaScript
- **Tailwind CSS**: Utility-first CSS framework
- **Vite**: Fast build tool
- **Axios**: HTTP client
- **React Dropzone**: File upload component
- **React Markdown**: Markdown rendering
- **React Syntax Highlighter**: Code syntax highlighting
- **Lucide React**: Icon library

## 🚀 Development Setup (Without Docker)

If you prefer to run without Docker for development:

### Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
# Copy .env from root (or create in backend/)
cp ../.env.example ../.env
# Edit ../.env with your MISTRAL_API_KEY
python main.py
```

**Note**: The backend will automatically look for `.env` in both the `backend/` directory and the root directory. You can use the same `.env` file for both Docker and non-Docker setups by placing it in the root directory.

The backend will be available at `http://localhost:8000`

### Frontend Setup

```bash
cd frontend
npm install --legacy-peer-deps
npm run dev
```

The frontend will be available at `http://localhost:3000`

**Note**: For production or easiest setup, we recommend using Docker Compose as shown above.

## 🐳 Docker Details

### Backend Dockerfile

- Uses Python 3.11 slim image
- Installs system dependencies
- Copies requirements and installs Python packages
- Exposes port 8000
- Runs with uvicorn

### Frontend Dockerfile

- Multi-stage build (builder + production)
- Uses Node.js 20 Alpine for building
- Uses Nginx Alpine for serving static files
- Includes proxy configuration for API calls
- Exposes port 3000

### Docker Compose

- Orchestrates both services
- Handles networking between containers
- Manages volumes for file uploads
- Includes health checks
- Auto-restarts on failure


## 🐛 Troubleshooting

### Common Issues

**Issue**: Docker build fails
- **Solution**: Ensure Docker and Docker Compose are up to date
- Check: `docker --version` and `docker compose version`

**Issue**: Mistral API errors
- **Solution**: Verify your `MISTRAL_API_KEY` is set correctly in `.env`
- Check: API key is valid at https://console.mistral.ai/
- Note: Without API key, app runs but AI features are unavailable

**Issue**: Frontend can't connect to backend
- **Solution**: Ensure both services are running
- Check: Backend at http://localhost:8000/health
- Check: Frontend at http://localhost:3000

**Issue**: Tests fail
- Ensure dependencies are installed: `pip install -r requirements.txt` and `npm install`

**Issue**: Port already in use
- **Solution**: Change ports in `docker-compose.yml` or stop conflicting services
- Backend default: 8000, Frontend default: 3000

## 📝 License

MIT License - See LICENSE file for details

## 🙏 Acknowledgments

- **Mistral AI** for providing powerful AI models
- **FastAPI** for the excellent web framework
- **React** team for the amazing UI library

## 📖 Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [React Documentation](https://react.dev/)
- [Mistral AI Documentation](https://docs.mistral.ai/)

---

**Built with ❤️ for Mistral AI Internship Application**
