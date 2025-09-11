from google.adk.agents import LlmAgent
from typing import Any, Dict

import time
import psutil



def get_memory_info() -> Dict[str, Any]:
    """
    Gather memory information including RAM and swap usage.

    Returns:
        Dict[str, Any]: Dictionary with memory information structured for ADK
    """
    try:
        memory = psutil.virtual_memory()
        swap = psutil.swap_memory()

        memory_info = {
            "total_memory": f"{memory.total / (1024 ** 3):.2f} GB",
            "available_memory": f"{memory.available / (1024 ** 3):.2f} GB",
            "used_memory": f"{memory.used / (1024 ** 3):.2f} GB",
            "memory_percentage": f"{memory.percent:.1f}%",
            "swap_total": f"{swap.total / (1024 ** 3):.2f} GB",
            "swap_used": f"{swap.used / (1024 ** 3):.2f} GB",
            "swap_percentage": f"{swap.percent:.1f}%",
        }

        memory_usage = memory.percent
        swap_usage = swap.percent
        high_memory_usage = memory_usage > 80
        high_swap_usage = swap_usage > 80
        
        return {
            "result": memory_info,
            "stats": {
                "memory_usage_percentage": memory_usage,
                "swap_usage_percentage": swap_usage,
                "total_memory_gb": memory.total / (1024**3),
                "available_memory_gb": memory.available / (1024**3),
            },
            "additional_info": {
                "data_format": "dictionary",
                "collection_timestamp": time.time(),
                "performance_concern": (
                    "High memory usage detected" if high_memory_usage else None
                ),
                "swap_concern": "High swap usage detected" if high_swap_usage else None,
            },
        }
    except Exception as e:
        return {
            "result": {"error": f"Failed to gather memory information: {str(e)}"},
            "stats": {"success": False},
            "additional_info": {"error_type": str(type(e).__name__)},
        }


memory_info_agent = LlmAgent(
    name="MemoryInfoAgent",
    model="gemini-2.0-flash",
    instruction="""You are a Memory Information Agent.
    
    When asked for system information, you should:
    1. Use the 'get_memory_info' tool to gather memory data
    2. Analyze the returned dictionary data
    3. Format this information into a concise, clear section of a system report
    
    The tool will return a dictionary with:
    - result: Core memory information
    - stats: Key statistical data about memory usage
    - additional_info: Context about the data collection
    
    Format your response as a well-structured report section with:
    - Total and available memory
    - Memory usage statistics
    - Swap memory information
    - Any performance concerns (high usage > 80%)
    
    IMPORTANT: You MUST call the get_memory_info tool. Do not make up information.
    """,
    description="Gathers and analyzes memory information",
    tools=[get_memory_info],
    output_key="memory_info",
)
