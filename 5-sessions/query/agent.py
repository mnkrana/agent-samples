from google.adk.agents import Agent

# Create the root agent
question_answering_agent = Agent(
    name="query_agent",
    model="gemini-2.0-flash",
    description="Question answering agent",
    instruction="""
    You are a helpful assistant that answers questions about the user's preferences.

    Here is some information about the user:
    Name: 
    {user_name}
    Preferences: 
    {user_preferences}
    """,
)
