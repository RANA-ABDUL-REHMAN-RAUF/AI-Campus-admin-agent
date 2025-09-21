from fastapi import APIRouter

router = APIRouter()
@router.post("/chat")
async def chat_endpoint(request: ChatRequest):
    result = await Runner.run(handoff_agent, request.query)
    # Make sure it's JSON serializable
    if hasattr(result, "output"):
        return {"response": str(result.output)}
    return {"response": str(result)}

# /chat/stream: Streaming chat responses (SSE)
@router.post("/chat/stream")
async def chat_stream_endpoint(request: ChatRequest):
    result = Runner.run_streamed(handoff_agent, input=request.query)

    async def event_generator():
        async for event in result.stream_events():
            if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
                yield event.data.delta

    return StreamingResponse(event_generator(), media_type="text/event-stream")

@router.post("/students")
async def students(request: ChatRequest):
    result = await Runner.run(student_management_agent, request.query)
    # Make sure it's JSON serializable
    if hasattr(result, "output"):
        return {"response": str(result.output)}
    return {"response": str(result)}


# /analytics: Returns JSON with statistics
@router.post("/analytics")
async def analytics_endpoint(request: ChatRequest):
    result = await Runner.run(campus_analytics_agent, request.query)
    # Make sure it's JSON serializable
    if hasattr(result, "output"):
        return {"response": str(result.output)}
    return {"response": str(result)}

# Example root endpoint
@router.get("/")
async def root():
    return {"message": "Campus Admin Agent API is running."}