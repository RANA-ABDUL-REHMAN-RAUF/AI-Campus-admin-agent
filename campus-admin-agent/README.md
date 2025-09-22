# 🏫 Campus AI Admin Agent

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)](https://fastapi.tiangolo.com)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0+-red.svg)](https://sqlalchemy.org)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![SMIT](https://img.shields.io/badge/SMIT-Hackathon-orange.svg)](https://smit.edu.pk)

> **An intelligent AI-powered campus administration system for Saylani Mass IT Training (SMIT) Center**

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [API Documentation](#api-documentation)
- [Project Structure](#project-structure)
- [Development](#development)
- [Contributing](#contributing)
- [License](#license)

## 🎯 Overview

The **Campus AI Admin Agent** is a sophisticated, multi-agent system designed to streamline campus administration tasks at Saylani Mass IT Training (SMIT) Center. Built with modern AI technologies and FastAPI, it provides intelligent assistance for student management, campus analytics, and facility information through natural language interactions.

### Key Highlights

- **🤖 Multi-Agent Architecture**: Specialized AI agents for different administrative tasks
- **📊 Real-time Analytics**: Comprehensive campus statistics and insights
- **🎓 Student Management**: Complete CRUD operations for student records
- **🏢 Campus Information**: Instant access to facility timings and services
- **🔍 RAG Integration**: Retrieval-Augmented Generation for contextual responses
- **⚡ FastAPI Backend**: High-performance REST API with streaming support
- **🗄️ Database Integration**: SQLAlchemy with support for SQLite and PostgreSQL

## ✨ Features

### 🎓 Student Management
- **Add Students**: Register new students with comprehensive validation
- **Retrieve Information**: Get student details by ID with error handling
- **Update Records**: Modify student information with field validation
- **Delete Students**: Remove student records with confirmation
- **List All Students**: View complete student directory with pagination

### 📈 Campus Analytics
- **Total Student Count**: Active/inactive breakdown with real-time updates
- **Department Distribution**: Student count by academic department
- **Recent Onboardings**: Latest student registrations with timestamps
- **Activity Tracking**: 7-day student activity analysis and insights

### 🏢 Campus Information
- **Cafeteria Services**: Complete timings, menu, and operating hours
- **Library Access**: Hours, study rooms, and facility information
- **SMIT Center Details**: Comprehensive campus information via RAG system

### 🔧 Technical Features
- **Multi-Agent Orchestration**: Intelligent query routing and handoff
- **Streaming Responses**: Real-time chat experience with SSE
- **Database Integration**: SQLAlchemy ORM with migration support
- **Input Validation**: Pydantic models with comprehensive sanitization
- **Comprehensive Logging**: Activity tracking and debugging capabilities
- **CORS Support**: Cross-origin resource sharing for web integration
- **Error Handling**: Graceful error management with user-friendly messages

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Git
- Database (SQLite/PostgreSQL)

### Step 1: Clone the Repository

```bash
git clone https://github.com/your-username/campus-ai-admin-agent.git
cd campus-ai-admin-agent/campus-admin-agent
```

### Step 2: Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
# Navigate to backend directory
cd backend

# Install required packages
pip install fastapi uvicorn sqlalchemy pydantic python-dotenv
pip install langchain langchain-community langchain-google-genai
pip install agents openai python-multipart
```

### Step 4: Environment Configuration

Create a `.env` file in the backend directory:

```env
# Database Configuration
DATABASE_URL=sqlite:///./campus_admin.db
# For PostgreSQL: postgresql://username:password@localhost/dbname

# AI Model Configuration
GEMINI_API_KEY=your_gemini_api_key_here
OPENAI_API_KEY=your_openai_api_key_here

# Application Settings
DEBUG=True
LOG_LEVEL=INFO
HOST=0.0.0.0
PORT=8000
```

## ⚙️ Configuration

### Database Setup

The application supports both SQLite (default) and PostgreSQL:

```python
# SQLite (Development)
DATABASE_URL=sqlite:///./campus_admin.db

# PostgreSQL (Production)
DATABASE_URL=postgresql://username:password@localhost:5432/campus_admin
```

### AI Model Configuration

Configure your preferred AI model:

```python
# Gemini (Recommended)
GEMINI_API_KEY=your_gemini_api_key

# OpenAI (Alternative)
OPENAI_API_KEY=your_openai_api_key
```

## 🎮 Usage

### Starting the Application

```bash
# Navigate to backend directory
cd backend

# Start the FastAPI server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The application will be available at:
- **API**: http://localhost:8000
- **Documentation**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc

### Example API Calls

#### General Chat
```bash
curl -X POST "http://localhost:8000/chat" \
     -H "Content-Type: application/json" \
     -d '{"query": "Hello, I need help with campus administration"}'
```

#### Student Management
```bash
# Add a new student
curl -X POST "http://localhost:8000/students" \
     -H "Content-Type: application/json" \
     -d '{"query": "Add a new student named John Doe with ID CS2024001, email john@example.com, department Computer Science"}'

# Get student information
curl -X POST "http://localhost:8000/students" \
     -H "Content-Type: application/json" \
     -d '{"query": "Get information for student CS2024001"}'
```

#### Campus Analytics
```bash
curl -X POST "http://localhost:8000/analytics" \
     -H "Content-Type: application/json" \
     -d '{"query": "Show me total student count by department"}'
```

## 📚 API Documentation

### Endpoints

| Endpoint | Method | Description | Parameters |
|----------|--------|-------------|------------|
| `/` | GET | Health check and welcome message | None |
| `/chat` | POST | Standard chat with AI agents | `{"query": "string"}` |
| `/chat/stream` | POST | Streaming chat responses | `{"query": "string"}` |
| `/students` | POST | Student management operations | `{"query": "string"}` |
| `/analytics` | POST | Campus analytics and statistics | `{"query": "string"}` |

### Request Format

```json
{
  "query": "Your question or command here"
}
```

### Response Format

```json
{
  "response": "AI agent response here"
}
```

## 📁 Project Structure

```
campus-admin-agent/
├── backend/
│   ├── app/
│   │   ├── agent/
│   │   │   └── agent.py              # Multi-agent system configuration
│   │   ├── api/
│   │   │   └── routes.py             # REST API endpoints
│   │   ├── models/
│   │   │   └── models.py             # SQLAlchemy database models
│   │   ├── services/
│   │   │   └── service.py            # Business logic layer
│   │   ├── Tools/
│   │   │   ├── Campus_analytics_tools.py    # Analytics functions
│   │   │   ├── FAQ_tools.py                 # Campus info functions
│   │   │   ├── RAG_tool.py                  # RAG implementation
│   │   │   ├── student _manegement_tool_.py # Student management
│   │   │   └── data/
│   │   │       └── SMIT.txt                 # Knowledge base
│   │   ├── utils/
│   │   │   └── pydentic_model.py     # Pydantic validation models
│   │   └── main.py                   # FastAPI application entry point
│   └── README.md                     # Backend documentation
└── README.md                        # This file
```

### Key Components

- **`main.py`**: FastAPI application with CORS middleware and routing
- **`agent.py`**: Multi-agent system with specialized AI agents
- **`routes.py`**: REST API endpoints with streaming support
- **`models.py`**: SQLAlchemy database models for students and activity logs
- **`Tools/`**: Specialized function tools for each agent type
- **`pydentic_model.py`**: Data validation and serialization models

## 🛠️ Development

### Adding New Features

1. **New Agent**: Create agent configuration in `app/agent/agent.py`
2. **New Tools**: Add function tools in appropriate `app/Tools/` files
3. **New Endpoints**: Extend `app/api/routes.py` with new API endpoints
4. **Database Changes**: Update models in `app/models/models.py`

### Code Quality

```bash
# Run linting
flake8 app/

# Run type checking
mypy app/

# Run tests (when implemented)
pytest tests/
```

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** your changes (`git commit -m 'Add amazing feature'`)
4. **Push** to the branch (`git push origin feature/amazing-feature`)
5. **Open** a Pull Request

### Development Guidelines

- Follow PEP 8 style guidelines
- Add type hints to all functions
- Include comprehensive docstrings
- Write tests for new features
- Update documentation as needed

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Saylani Mass IT Training (SMIT)** for providing the platform and requirements
- **FastAPI** team for the excellent web framework
- **LangChain** community for RAG implementation guidance
- **Google Gemini** for AI model capabilities
- **SQLAlchemy** team for robust ORM functionality

## 📞 Support

For support and questions:

- **Email**: support@smit.edu.pk
- **Issues**: [GitHub Issues](https://github.com/your-username/campus-ai-admin-agent/issues)
- **Documentation**: [Wiki](https://github.com/your-username/campus-ai-admin-agent/wiki)

---

<div align="center">

**Built with ❤️ for SMIT Hackathon**

[🏠 Home](https://smit.edu.pk) | [📖 Docs](docs/) | [🐛 Report Bug](issues/) | [💡 Request Feature](issues/)

</div>