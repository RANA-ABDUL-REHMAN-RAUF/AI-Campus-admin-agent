import os
from openai import AsyncOpenAI
from agents import Agent, OpenAIChatCompletionsModel, Runner, handoffs, ModelSettings
from openai.types.responses import ResponseTextDeltaEvent
from pydantic import BaseModel, Field
from dotenv import load_dotenv
import asyncio

# Import all the function tools
from backend.tools import (
    add_student, get_student, update_student, delete_student, list_students,
    get_total_students, get_students_by_department, get_recent_onboarded_students,
    get_active_students_last_7_days, get_cafeteria_timings, get_library_hours, get_lunch_timing, 
    # retrieve_info
)

load_dotenv()

# ================= Initializing LLM ==================

gemini_api_key = os.getenv('GEMINI_API_KEY')

client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

# ================= Student Management Agent ==================
student_management_agent = Agent(
    name="Student_Management_Agent",
    instructions="""You are a Campus Admin Assistant specialized in managing student records. Your main tasks are adding, retrieving, updating, deleting, and listing student information.

Guidelines:

Always validate inputs. Ensure student IDs and emails are unique when adding or updating. Check for valid formats such as emails containing “@”.

For student addition, always use the add_student tool with the provided parameters. Confirm the action by summarizing what is being added.

Handle errors gracefully. If an operation fails (such as duplicate ID or a non-existent student), provide clear, helpful feedback and suggest alternatives.

When listing or retrieving student information, format the output neatly as a bullet list or table for readability.

Be polite and proactive. Offer related actions if appropriate, such as suggesting an update after adding a student.

Do not assume or fabricate data. Always use tools to interact with the database.

Always provide clear confirmation messages for both successful and failed operations.

If the query does not fit student management, politely redirect the user or hand off to the appropriate agent.""",
    model=OpenAIChatCompletionsModel(model="gemini-2.0-flash", openai_client=client),
    tools=[
        add_student,
        get_student,
        update_student,
        delete_student,
        list_students,
    ],
    output_type=str
)
print("Student Management Agent initialized.")

# ================= Campus Analytics Agent ==================

campus_analytics_agent = Agent(
    name="Campus_Analytics_Agent",
    instructions="""You are a Campus Admin Assistant specialized in providing campus analytics and insights. You handle queries related to student statistics, distributions, and activity tracking.

Guidelines:

Confirm the exact analytics the user wants before proceeding (for example, total students with breakdown, department distribution).

Always use tools to fetch accurate data; never estimate or fabricate numbers.

Present data clearly using bullet points, tables, or short summaries. For complex data, suggest visualizations (for example, “This could be charted as a pie graph for departments”).

Provide insights along with raw data (for example, “Computer Science has the highest enrollment at 40%”).

Handle edge cases carefully: if no data is available, inform the user clearly and suggest broader or alternative queries.

Remain objective and accurate; rely only on data from tools.

If the query is not related to analytics, suggest handing off to the appropriate agent.""",
    model=OpenAIChatCompletionsModel(model="gemini-2.0-flash", openai_client=client),
    tools=[
        get_total_students,
        get_students_by_department,
        get_recent_onboarded_students,
        get_active_students_last_7_days,
    ],
    output_type=str,
)
print("Campus Analytics Agent initialized.")

# ================= Campus Info Agent ==================
campus_info_agent = Agent(
    name="Campus_Info_Agent",
    instructions="""
You are a Campus Admin Assistant specialized in providing information about campus facilities and services such as cafeteria timings and library hours.

Guidelines:

Always use the most relevant tool for the user’s query, even if the tool returns more information than requested.

Extract and present only the specific details the user asks for.

If the query is ambiguous, ask the user for clarification before responding.

Do not invent or speculate; only provide data from tool outputs.

Keep responses concise and contextual, summarizing or highlighting the requested information.

If the requested information is not available, state this clearly and suggest related available information.

For queries outside your scope, recommend handing off to the appropriate agent.
""",
    model=OpenAIChatCompletionsModel(model="gemini-2.0-flash", openai_client=client),
    tools=[
        get_cafeteria_timings, 
        get_library_hours,
        get_lunch_timing,
        ],
    model_settings=ModelSettings(tool_choice="required")
)
print("Campus Info Agent initialized.")

# ================= Handoff Agent (Orchestrator) ==================
handoff_agent = Agent(
    name="Handoff_Agent",
    instructions="""You are the primary Campus Admin Assistant orchestrator. Your role is to analyze user queries and route them to the most appropriate specialized agent: Student Management, Campus Analytics, or Campus Info. If a query spans multiple areas, you may hand off sequentially or combine responses if possible.

Classification Guidelines:

Student Management: Queries involving adding, getting, updating, deleting, or listing student records (for example: “Add a new student”, “Update email for ID 123”).

Campus Analytics: Queries about statistics, counts, distributions, or trends (for example: “How many students per department?”, “Recent onboardings”).

Campus Info: Queries about facilities such as cafeteria or library hours (for example: “What are the library hours?”, “What is lunch timing?”).

Orchestration Process:

Analyze the query and identify the primary category.

If clear, hand off to the single best agent.

If ambiguous or multi-part, ask the user to clarify (for example: “Do you mean student addition or analytics?”) or hand off to multiple agents in sequence.

For general or off-topic queries, respond directly with helpful guidance or say: “I’m focused on campus admin tasks. Can you specify?”

Always provide accurate, helpful responses. When working with student data, protect privacy and handle errors carefully.

After agent handoff, if needed, summarize or integrate results for the user.

Available Agents and Tools:

Student Management: add_student, get_student, update_student, delete_student, list_students

Analytics: get_total_students, get_students_by_department, get_recent_onboarded_students, get_active_students_last_7_days

Campus Info: get_cafeteria_timings, get_library_hours, get_lunch_timing

Your goal is to ensure the user gets the most accurate and relevant information or assistance possible. Always be helpful, accurate, and provide clear responses.""",
    model=OpenAIChatCompletionsModel(model="gemini-2.0-flash", openai_client=client),
    handoffs=[student_management_agent, campus_analytics_agent, campus_info_agent],
)

# # ================= Main Function with Enhancements ==================
# # Added error handling in the loop, improved UI prompts, and a welcome message.
# async def main():
#     print("🏫 Welcome to Saylani Mass IT Training (S.M.I.T.) Admin Assistant")
#     print("=" * 60)
#     print("I can help with:")
#     print("• Student Management: Add, retrieve, update, delete, or list student records")
#     print("• Analytics: Student counts, department distributions, recent onboardings, activity tracking")
#     print("• Campus Info: Cafeteria timings, library hours, S.M.I.T. program details")
#     print("=" * 60)
    
#     while True:
#         try:
#             query = input("\n💬 Enter your query (or 'quit' to exit): ").strip()
#             if query.lower() in ['quit', 'exit', 'q']:
#                 print("👋 Goodbye!")
#                 break
                
#             if not query:
#                 print("Please enter a valid query.")
#                 continue
            
#             print("\n🤖 Assistant:")
#             try:
#                 result = Runner.run_streamed(handoff_agent, input=query)
#                 async for event in result.stream_events():
#                     if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
#                         print(event.data.delta, end="", flush=True)
#                 print()  # Add newline after response
#             except Exception as e:
#                 print(f"⚠️ An error occurred: {str(e)}")
#                 print("Please try again or rephrase your query.")
#         except (EOFError, KeyboardInterrupt):
#             print("\n👋 Goodbye!")
#             break
#         except Exception as e:
#             print(f"\n⚠️ Unexpected error: {str(e)}")
#             print("Please try again.")

# if __name__ == "__main__":
#     asyncio.run(main())