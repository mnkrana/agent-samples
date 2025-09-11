from google.adk.agents import LlmAgent
from typing import Any, Dict
import time
import psutil


def get_cpu_info() -> Dict[str, Any]:
    """
    Gather CPU information including core count and usage.

    Returns:
        Dict[str, Any]: Dictionary with CPU information structured for ADK
    """
    try:        
        cpu_info = {
            "physical_cores": psutil.cpu_count(logical=False),
            "logical_cores": psutil.cpu_count(logical=True),
            "cpu_usage_per_core": [
                f"Core {i}: {percentage:.1f}%"
                for i, percentage in enumerate(
                    psutil.cpu_percent(interval=1, percpu=True)
                )
            ],
            "avg_cpu_usage": f"{psutil.cpu_percent(interval=1):.1f}%",
        }
        
        avg_usage = float(cpu_info["avg_cpu_usage"].strip("%"))
        high_usage = avg_usage > 80
        
        return {
            "result": cpu_info,
            "stats": {
                "physical_cores": cpu_info["physical_cores"],
                "logical_cores": cpu_info["logical_cores"],
                "avg_usage_percentage": avg_usage,
                "high_usage_alert": high_usage,
            },
            "additional_info": {
                "data_format": "dictionary",
                "collection_timestamp": time.time(),
                "performance_concern": (
                    "High CPU usage detected" if high_usage else None
                ),
            },
        }
    except Exception as e:
        return {
            "result": {"error": f"Failed to gather CPU information: {str(e)}"},
            "stats": {"success": False},
            "additional_info": {"error_type": str(type(e).__name__)},
        }


cpu_info_agent = LlmAgent(
    name="CpuInfoAgent",
    model="gemini-2.0-flash",
    instruction="""You are a CPU Information Agent.
    
    When asked for system information, you should:
    1. Use the 'get_cpu_info' tool to gather CPU data
    2. Analyze the returned dictionary data
    3. Format this information into a concise, clear section of a system report
    
    The tool will return a dictionary with:
    - result: Core CPU information
    - stats: Key statistical data about CPU usage
    - additional_info: Context about the data collection
    
    Format your response as a well-structured report section with:
    - CPU core information (physical vs logical)
    - CPU usage statistics
    - Any performance concerns (high usage > 80%)
    
    IMPORTANT: You MUST call the get_cpu_info tool. Do not make up information.
    """,
    description="Gathers and analyzes CPU information",
    tools=[get_cpu_info],
    output_key="cpu_info",
)
