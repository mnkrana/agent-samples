from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool

from .tools.tools import get_current_time
from .sub_agents.joke_agent.agent import joke_agent
from .sub_agents.news_analyst.agent import news_analyst
from .sub_agents.stock_analyst.agent import stock_analyst

root_agent = Agent(
    name="manager_agent",
    model="gemini-2.0-flash",
    description="Manager agent",
    instruction="""
    You are a manager agent that is responsible for overseeing the work of the other agents.

    Always delegate the task to the appropriate agent. Use your best judgement 
    to determine which agent to delegate to.

    You are responsible for delegating tasks to the following agent:    
    - joke_agent
    - stock_analyst

    You also have access to the following tools:    
    - get_current_time
    - news_analyst
    """,
    sub_agents=[joke_agent, stock_analyst],
    tools=[        
        get_current_time,
        AgentTool(news_analyst)
    ],
)
