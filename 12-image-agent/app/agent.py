from google.adk.agents import SequentialAgent

from .subagents.prompt_agent.agent import prompt_agent
from .subagents.image_gen_agent.agent import image_gen_agent 

root_agent = SequentialAgent(
    name="image_agent",    
    sub_agents=[prompt_agent, image_gen_agent],
    description="Image generation agent",        
)