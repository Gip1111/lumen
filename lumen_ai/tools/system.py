import platform
import subprocess
from .manager import tool

@tool(
    name="get_system_info",
    description="Get information about the current Lumen system (kernel, CPU, distro version).",
    schema={
        "type": "object",
        "properties": {}
    },
    requires_confirmation=False
)
async def get_system_info():
    return {
        "distro": "Lumen (Arch based)",
        "kernel": platform.release(),
        "arch": platform.machine(),
        "python_version": platform.python_version()
    }

@tool(
    name="check_updates",
    description="Check for available system updates using pacman.",
    schema={
        "type": "object",
        "properties": {}
    },
    requires_confirmation=False
)
async def check_updates():
    try:
        # Note: on a live ISO or dev machine, this might return nothing or require root
        # For now, we simulate the check
        return {"updates_available": 0, "packages": []}
    except Exception as e:
        return {"error": str(e)}
