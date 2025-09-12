import asyncio 
import vertexai
from vertexai import agent_engines
from tool_agent.agent import root_agent

PROJECT_ID = "agents-demo-471909"
LOCATION = "us-central1"
STAGING_BUCKET = "gs://agents-demo"

vertexai.init(
    project=PROJECT_ID,
    location=LOCATION,
    staging_bucket=STAGING_BUCKET,
)

app = agent_engines.AdkApp(
    agent=root_agent,
    enable_tracing=True,
)

async def main():
    session = await app.async_create_session(user_id="u_123")
    print(session)

    events = []
    async for event in app.async_stream_query(
        user_id="u_123",
        session_id=session.id,
        message="whats the weather in delhi",
    ):
        events.append(event)

    # The full event stream shows the agent's thought process
    # print("--- Full Event Stream ---")
    # for event in events:
    #     print(event)

    # For quick tests, you can extract just the final text response
    final_text_responses = [
        e for e in events
        if e.get("content", {}).get("parts", [{}])[0].get("text")
        and not e.get("content", {}).get("parts", [{}])[0].get("function_call")
    ]
    if final_text_responses:
        print("\n--- Final Response ---")
        print(final_text_responses[0]["content"]["parts"][0]["text"])

if __name__ == "__main__":
    asyncio.run(main())