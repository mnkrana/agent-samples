import asyncio

from dotenv import load_dotenv
from google.adk.runners import Runner
from google.adk.sessions import DatabaseSessionService
from google.genai import types

from course_agent.agent import course_agent

load_dotenv()

db_url = "sqlite:///./courses.db"
session_service = DatabaseSessionService(db_url=db_url)

inital_state = {
    "user_name": "Mayank Rana",
    "purchased_courses" : [],
    "interaction_history": [],
}

async def main():
    print("\nWelcome to Customer Service Chat!")
    APP_NAME = "course agent"
    USER_ID = "mayank_rana"

    existing_sessions = await session_service.list_sessions(app_name=APP_NAME, user_id=USER_ID)

    if existing_sessions and len(existing_sessions.sessions) > 0:
        SESSION_ID = existing_sessions.sessions[0].id
        print(f"\nexisting session found: {SESSION_ID}\n")
    else:
        new_session = await session_service.create_session(app_name=APP_NAME, user_id=USER_ID, state=inital_state)
        SESSION_ID = new_session.id
        print(f"\ncreating new session: {SESSION_ID}\n")

    runner = Runner(app_name=APP_NAME, agent=course_agent, session_service=session_service)

    while True:
        user_input = input("You: ")

        if user_input.lower() in ["exit", "quit"]:
            break

        await call_agent_async(runner, USER_ID, SESSION_ID, user_input)

async def call_agent_async(runner: Runner, user_id, session_id, user_input):
    content = types.Content(role="user", parts=[types.Part(text=user_input)])

    async for event in runner.run_async(user_id=user_id, session_id=session_id, new_message=content):
        if event.is_final_response():
            if event.content and event.content.parts and hasattr(event.content.parts[0], "text") and event.content.parts[0].text:
                print(f"\nAgent: {event.content.parts[0].text.strip()}")
                return event.content.parts[0].text.strip()

    
if __name__ == "__main__":
    asyncio.run(main())