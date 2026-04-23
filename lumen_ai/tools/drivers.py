from .manager import tool
from lumen_drivers.manager import driver_manager

@tool(
    name="scan_hardware",
    description="Scan the system for PCI hardware devices.",
    schema={
        "type": "object",
        "properties": {}
    },
    requires_confirmation=False
)
async def scan_hardware():
    return {"devices": driver_manager.scan_pci()}

@tool(
    name="get_driver_recommendations",
    description="Get recommended drivers for the detected hardware.",
    schema={
        "type": "object",
        "properties": {}
    },
    requires_confirmation=False
)
async def get_driver_recommendations():
    return {"recommendations": driver_manager.get_recommendations()}
@tool(
    name="install_recommended_driver",
    description="Install a recommended driver for a specific hardware device.",
    schema={
        "type": "object",
        "properties": {
            "driver_name": {"type": "string", "description": "The name of the driver to install (e.g., 'nvidia')"}
        },
        "required": ["driver_name"]
    },
    requires_confirmation=True
)
async def install_recommended_driver(driver_name: str):
    return driver_manager.install_driver(driver_name)
