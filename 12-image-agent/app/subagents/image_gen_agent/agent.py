from google.adk.agents import Agent
from .image_gen_tool import generate_images

image_gen_agent = Agent(
    name="image_gen_agent",
    model="gemini-2.0-flash",
    description="Generates an image from a detailed prompt.",    
    instruction="""You are an image generation agent.    
    You must call the `generate_image` tool with the prompt: {generated_prompt}
    """,
    tools=[generate_images],
    output_key="generated_image",
)