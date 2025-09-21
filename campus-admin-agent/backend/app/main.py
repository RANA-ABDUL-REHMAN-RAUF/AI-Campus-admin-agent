from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from agents import Runner

from pydantic import BaseModel
from backend.agent import handoff_agent, student_management_agent, campus_analytics_agent   # if you actually have backend/agent.py
from openai.types.responses import ResponseTextDeltaEvent

app = FastAPI()

# Example CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# /chat: Normal chat (async/await)
class ChatRequest(BaseModel):
    query: str

