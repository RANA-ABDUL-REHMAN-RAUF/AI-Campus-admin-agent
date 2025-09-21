# 🏫 Campus AI Admin Agent

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)](https://fastapi.tiangolo.com)
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
- [Contributing](#contributing)
- [License](#license)

## 🎯 Overview

The **Campus AI Admin Agent** is a sophisticated, multi-agent system designed to streamline campus administration tasks at Saylani Mass IT Training (SMIT) Center. Built with modern AI technologies, it provides intelligent assistance for student management, campus analytics, and facility information through natural language interactions.

### Key Highlights

- **🤖 Multi-Agent Architecture**: Specialized AI agents for different administrative tasks
- **📊 Real-time Analytics**: Comprehensive campus statistics and insights
- **🎓 Student Management**: Complete CRUD operations for student records
- **🏢 Campus Information**: Instant access to facility timings and services
- **🔍 RAG Integration**: Retrieval-Augmented Generation for contextual responses
- **⚡ FastAPI Backend**: High-performance REST API with streaming support

## ✨ Features

### 🎓 Student Management
- **Add Students**: Register new students with validation
- **Retrieve Information**: Get student details by ID
- **Update Records**: Modify student information
- **Delete Students**: Remove student records
- **List All Students**: View complete student directory

### 📈 Campus Analytics
- **Total Student Count**: Active/inactive breakdown
- **Department Distribution**: Student count by academic department
- **Recent Onboardings**: Latest student registrations
- **Activity Tracking**: 7-day student activity analysis

### 🏢 Campus Information
- **Cafeteria Services**: Timings, menu, and operating hours
- **Library Access**: Hours, study rooms, and facilities
- **SMIT Center Details**: Comprehensive campus information via RAG

### 🔧 Technical Features
- **Multi-Agent Orchestration**: Intelligent query routing
- **Streaming Responses**: Real-time chat experience
- **Database Integration**: SQLAlchemy with PostgreSQL/SQLite
- **Input Validation**: Pydantic models with sanitization
- **Comprehensive Logging**: Activity tracking and debugging
- **CORS Support**: Cross-origin resource sharing

## 🏗️ Architecture

```mermaid
graph TB
    A[User Interface] --> B[FastAPI Backend]
    B --> C[Handoff Agent]
    C --> D[Student Management Agent]
    C --> E[Campus Analytics Agent]
    C --> F[Campus Info Agent]
    C --> G[RAG Agent]
    
    D --> H[Student Tools]
    E --> I[Analytics Tools]
    F --> J[FAQ Tools]
    G --> K[Knowledge Base]
    
    H --> L[Database]
    I --> L
    J --> M[Static Data]
    K --> N[SMIT.txt]
    
    style A fill:#e1f5fe
    style B fill:#f3e5f5
    style C fill:#fff3e0
    style D fill:#e8f5e8
    style E fill:#e8f5e8
    style F fill:#e8f5e8
    style G fill:#e8f5e8
```

### Agent Specialization

1. **Handoff Agent**: Primary orchestrator that routes queries to specialized agents
2. **Student Management Agent**: Handles all student-related operations
3. **Campus Analytics Agent**: Provides statistical insights and reports
4. **Campus Info Agent**: Manages facility information and FAQs
5. **RAG Agent**: Retrieves contextual information from knowledge base

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Git

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
# Install required packages
pip install -r requirements.txt
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

#### Chat Endpoint
```bash
curl -X POST "http://localhost:8000/chat" \
     -H "Content-Type: application/json" \
     -d '{"query": "Add a new student named John Doe with ID CS2024001"}'
```

#### Student Management
```bash
curl -X POST "http://localhost:8000/students" \
     -H "Content-Type: application/json" \
     -d '{"query": "List all students in Computer Science department"}'
```

#### Campus Analytics
```bash
curl -X POST "http://localhost:8000/analytics" \
     -H "Content-Type: application/json" \
     -d '{"query": "Show me total student count by department"}'
```

### Streaming Chat

For real-time responses:

```bash
curl -X POST "http://localhost:8000/chat/stream" \
     -H "Content-Type: application/json" \
     -d '{"query": "What are the cafeteria timings?"}'
```

## 📚 API Documentation

### Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Health check and welcome message |
| `/chat` | POST | Standard chat with AI agents |
| `/chat/stream` | POST | Streaming chat responses |
| `/students` | POST | Student management operations |
| `/analytics` | POST | Campus analytics and statistics |

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
│   │   │   └── agent.py              # AI agent configurations
│   │   ├── api/
│   │   │   └── routes.py             # API endpoints
│   │   ├── models/
│   │   │   └── models.py             # Database models
│   │   ├── services/
│   │   │   └── service.py            # Business logic
│   │   ├── Tools/
│   │   │   ├── Campus_analytics_tools.py    # Analytics functions
│   │   │   ├── FAQ_tools.py                 # Campus info functions
│   │   │   ├── RAG_tool.py                  # RAG implementation
│   │   │   ├── student _manegement_tool_.py # Student management
│   │   │   └── data/
│   │   │       └── SMIT.txt                 # Knowledge base
│   │   ├── utils/
│   │   │   └── pydentic_model.py     # Pydantic models
│   │   └── main.py                   # FastAPI application
│   └── README.md                     # Backend documentation
├── requirements.txt                  # Python dependencies
└── README.md                        # This file
```

### Key Components

- **`agent.py`**: Multi-agent system configuration and orchestration
- **`routes.py`**: REST API endpoints with streaming support
- **`models.py`**: SQLAlchemy database models
- **`Tools/`**: Specialized function tools for each agent
- **`pydentic_model.py`**: Data validation and serialization models

## 🛠️ Development

### Adding New Features

1. **New Agent**: Create agent configuration in `agent.py`
2. **New Tools**: Add function tools in appropriate `Tools/` files
3. **New Endpoints**: Extend `routes.py` with new API endpoints
4. **Database Changes**: Update models in `models.py`

### Code Quality

```bash
# Run linting
flake8 backend/

# Run type checking
mypy backend/

# Run tests
pytest backend/tests/
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