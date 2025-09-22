# Campus Administration Agent — Backend

A FastAPI-based backend for the Campus AI Admin Agent. It exposes REST endpoints that orchestrate specialized AI agents, manage student records, and provide campus analytics.

## Project Structure

- `app/`
  - `main.py` — FastAPI entrypoint, CORS, and router registration
  - `api/routes.py` — Public API endpoints (chat, streaming, students, analytics)
  - `agent/agent.py` — AI agents configuration and orchestration
  - `models/models.py` — SQLAlchemy ORM models and DB session setup
  - `services/service.py` — Placeholder for domain/business logic
  - `Tools/` — Function tools invoked by agents
    - `Campus_analytics_tools.py`
    - `FAQ_tools.py`
    - `RAG_tool.py`
    - `student _manegement_tool_.py`
    - `data/SMIT.txt`
  - `utils/pydentic_model.py` — Pydantic request/response models and helpers

## Prerequisites

- Python 3.8+
- A virtual environment tool (venv, uv, or similar)

## Installation

Using pip and venv:
```bash
cd campus-admin-agent/backend
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
pip install fastapi uvicorn sqlalchemy pydantic python-dotenv agents openai
```

Using uv (optional, recommended):
```powershell
cd campus-admin-agent\backend
uv add fastapi uvicorn sqlalchemy pydantic python-dotenv agents openai
```

## Configuration

Create a `.env` file in `backend/` with your database connection string. The backend recognizes any of the following (checked in this order):

```env
# Preferred
DATABASE-URI=sqlite:///./campus_admin.db
# Alternatives
# DATABASE_URI=sqlite:///./campus_admin.db
# DATABASE_URL=sqlite:///./campus_admin.db

# Optional AI keys if you plan to use agent features
GEMINI_API_KEY=your_key
OPENAI_API_KEY=your_key
```

## Initialize the Database (SQLite example)

```powershell
# PowerShell (handles the hyphen in the var name)
[Environment]::SetEnvironmentVariable("DATABASE-URI","sqlite:///./campus_admin.db","Process")
uv run python app\models\models.py
```

## Run the API

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
# or with uv
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

- API root: http://localhost:8000
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Contributing

Pull requests are welcome. Please add tests where appropriate and keep documentation up to date.

## License

MIT — see the root `LICENSE`.