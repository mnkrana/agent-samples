from google.adk.agents import ParallelAgent, SequentialAgent

from .subagents.cpu_info_agent.agent import cpu_info_agent
from .subagents.disk_info_agent.agent import disk_info_agent
from .subagents.memory_info_agent.agent import memory_info_agent
from .subagents.synthesizer_agent.agent import system_report_synthesizer

system_info_gatherer = ParallelAgent(
    name="system_info_gatherer",
    sub_agents=[cpu_info_agent, disk_info_agent, memory_info_agent],
)

root_agent = SequentialAgent(
    name="system_monitor_agent",
    sub_agents=[system_info_gatherer, system_report_synthesizer],
)
