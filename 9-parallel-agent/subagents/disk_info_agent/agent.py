from google.adk.agents import LlmAgent
from typing import Any, Dict

import time
import psutil


def get_disk_info() -> Dict[str, Any]:
    """
    Gather disk information including partitions and usage.

    Returns:
        Dict[str, Any]: Dictionary with disk information structured for ADK
    """
    try:        
        disk_info = {"partitions": []}
        partitions_over_threshold = []
        total_space = 0
        used_space = 0

        for partition in psutil.disk_partitions():
            try:
                partition_usage = psutil.disk_usage(partition.mountpoint)
                
                if partition_usage.percent > 85:
                    partitions_over_threshold.append(
                        f"{partition.mountpoint} ({partition_usage.percent:.1f}%)"
                    )
                
                total_space += partition_usage.total
                used_space += partition_usage.used

                disk_info["partitions"].append(
                    {
                        "device": partition.device,
                        "mountpoint": partition.mountpoint,
                        "filesystem_type": partition.fstype,
                        "total_size": f"{partition_usage.total / (1024 ** 3):.2f} GB",
                        "used": f"{partition_usage.used / (1024 ** 3):.2f} GB",
                        "free": f"{partition_usage.free / (1024 ** 3):.2f} GB",
                        "percentage": f"{partition_usage.percent:.1f}%",
                    }
                )
            except (PermissionError, FileNotFoundError):                
                pass
        
        overall_usage_percent = (
            (used_space / total_space * 100) if total_space > 0 else 0
        )
        
        return {
            "result": disk_info,
            "stats": {
                "partition_count": len(disk_info["partitions"]),
                "total_space_gb": total_space / (1024**3),
                "used_space_gb": used_space / (1024**3),
                "overall_usage_percent": overall_usage_percent,
                "partitions_with_high_usage": len(partitions_over_threshold),
            },
            "additional_info": {
                "data_format": "dictionary",
                "collection_timestamp": time.time(),
                "high_usage_partitions": (
                    partitions_over_threshold if partitions_over_threshold else None
                ),
            },
        }
    except Exception as e:
        return {
            "result": {"error": f"Failed to gather disk information: {str(e)}"},
            "stats": {"success": False},
            "additional_info": {"error_type": str(type(e).__name__)},
        }


disk_info_agent = LlmAgent(
    name="DiskInfoAgent",
    model="gemini-2.0-flash",
    instruction="""You are a Disk Information Agent.
    
    When asked for system information, you should:
    1. Use the 'get_disk_info' tool to gather disk data
    2. Analyze the returned dictionary data
    3. Format this information into a concise, clear section of a system report
    
    The tool will return a dictionary with:
    - result: Core disk information including partitions
    - stats: Key statistical data about storage usage
    - additional_info: Context about the data collection
    
    Format your response as a well-structured report section with:
    - Partition information
    - Storage capacity and usage
    - Any storage concerns (high usage > 85%)
    
    IMPORTANT: You MUST call the get_disk_info tool. Do not make up information.
    """,
    description="Gathers and analyzes disk information",
    tools=[get_disk_info],
    output_key="disk_info",
)
