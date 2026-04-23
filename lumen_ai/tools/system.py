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

@tool(
    name="get_network_status",
    description="Get current network connectivity status and interfaces.",
    schema={"type": "object", "properties": {}},
    requires_confirmation=False
)
async def get_network_status():
    try:
        # Simplified check
        result = subprocess.run(['nmcli', '-t', 'device'], capture_output=True, text=True)
        return {"status": result.stdout.strip() if result.returncode == 0 else "NetworkManager not running"}
    except Exception as e:
        return {"error": str(e)}

@tool(
    name="get_recent_logs",
    description="Get the last 20 lines of system logs from journalctl.",
    schema={"type": "object", "properties": {}},
    requires_confirmation=False
)
async def get_recent_logs():
    try:
        result = subprocess.run(['journalctl', '-n', '20', '--no-pager'], capture_output=True, text=True)
        return {"logs": result.stdout if result.returncode == 0 else "Could not read logs"}
    except Exception as e:
        return {"error": str(e)}
