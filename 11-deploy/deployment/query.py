import asyncio 
import vertexai
from vertexai import agent_engines

USER_ID="mayank_rana"
QUERY="who is mayank rana with over 13 years of experience?"
RESOURCE_NAME="projects/754673837740/locations/us-central1/reasoningEngines/7103236541572448256"

async def main():
    remote_app = agent_engines.get(RESOURCE_NAME)
    remote_session = await remote_app.async_create_session(user_id=USER_ID)
    print(remote_session)

    print(f"Sending query: {QUERY}")
    events = []
    async for event in remote_app.async_stream_query(
    user_id=USER_ID,
    session_id=remote_session["id"],
    message=QUERY,
    ):
        events.append(event)

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