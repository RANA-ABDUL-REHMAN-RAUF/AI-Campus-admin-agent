# mock_agents/__init__.py

import asyncio
from typing import Any, Callable, Dict, List, Optional, Type, TypeVar, AsyncGenerator

# Placeholder for ResponseTextDeltaEvent (if needed, otherwise can be simplified)
class ResponseTextDeltaEvent:
    def __init__(self, delta: str):
        self.delta = delta
    
    @property
    def type(self):
        return "raw_response_event"

# Generic placeholder for ModelSettings (adjust as needed)
class ModelSettings:
    def __init__(self, **kwargs):
        pass

# Generic placeholder for Model (adjust as needed)
class OpenAIChatCompletionsModel:
    def __init__(self, model: str, openai_client: Any):
        self.model = model
        self.openai_client = openai_client

# Generic placeholder for Agent
class Agent:
    def __init__(
        self, name: str, instructions: str, model: OpenAIChatCompletionsModel, 
        tools: Optional[List[Callable]] = None, output_type: Type = str, 
        handoffs: Optional[List["Agent"]] = None, model_settings: Optional[ModelSettings] = None
    ):
        self.name = name
        self.instructions = instructions
        self.model = model
        self.tools = tools if tools is not None else []
        self.output_type = output_type
        self.handoffs = handoffs if handoffs is not None else []
        self.model_settings = model_settings

    async def _run_tool(self, tool_func: Callable, **kwargs) -> Any:
        # Placeholder for tool execution logic
        print(f"Executing mock tool: {tool_func.__name__} with args: {kwargs}")
        # In a real scenario, you'd call the actual tool function here
        # For now, return a generic success message or mock data
        return {"success": True, "message": f"Mock execution of {tool_func.__name__} completed."}

    async def process_input(self, input_text: str) -> str:
        # Simple mock logic for processing input and potentially calling a tool
        print(f"Mock Agent '{self.name}' received: {input_text}")
        if "add student" in input_text.lower() and "add_student" in [t.__name__ for t in self.tools]:
            # Example: call mock add_student if it's in the tools list
            # This would need to be more sophisticated to parse arguments from input_text
            # For now, just simulate a tool call
            return (await self._run_tool(next(t for t in self.tools if t.__name__ == "add_student"), 
                                        name="Mock Student", student_id="MOCK123", 
                                        department="Mock Dept", email="mock@example.com"))
        
        # Basic instruction-based response or handoff simulation
        if self.handoffs:
            for handoff_agent in self.handoffs:
                if handoff_agent.name.lower().replace("_", " ") in input_text.lower():
                    print(f"Handoff to mock {handoff_agent.name}")
                    return await handoff_agent.process_input(input_text)
        
        return f"Mock response from {self.name}: I processed \"{input_text}\"."

# Generic placeholder for Runner
class Runner:
    @staticmethod
    async def run_streamed(agent: Agent, input: str) -> AsyncGenerator[Any, None]:
        # Simulate streaming a response character by character
        response = await agent.process_input(input)
        for char in response:
            await asyncio.sleep(0.01)  # Simulate delay
            yield ResponseTextDeltaEvent(delta=char)

# Generic placeholder for handoffs (if it's a specific object, otherwise it's just a list/tuple)
handoffs: Any = [] # This will be replaced by actual agent instances in main.py

# Placeholder for function_tool decorator
def function_tool(func: Callable) -> Callable:
    """A mock decorator that simply returns the decorated function."""
    return func
