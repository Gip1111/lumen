import functools
import inspect
from typing import Dict, Any, Callable, List

class ToolRegistry:
    """Manages system tools exposed to the AI assistant."""
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ToolRegistry, cls).__new__(cls)
            cls._instance.tools = {}
        return cls._instance
    
    def register(self, name: str, description: str, schema: Dict[str, Any], requires_confirmation: bool = True):
        def decorator(func: Callable):
            @functools.wraps(func)
            async def wrapper(*args, **kwargs):
                return await func(*args, **kwargs)
            
            self.tools[name] = {
                "func": wrapper,
                "description": description,
                "schema": schema,
                "requires_confirmation": requires_confirmation
            }
            return wrapper
        return decorator

    def get_tool_definitions(self) -> List[Dict[str, Any]]:
        """Returns JSON schemas for all registered tools."""
        return [
            {
                "type": "function",
                "function": {
                    "name": name,
                    "description": info["description"],
                    "parameters": info["schema"]
                }
            }
            for name, info in self.tools.items()
        ]

registry = ToolRegistry()

def tool(name: str, description: str, schema: Dict[str, Any], requires_confirmation: bool = True):
    """Decorator to register a tool."""
    return registry.register(name, description, schema, requires_confirmation)
