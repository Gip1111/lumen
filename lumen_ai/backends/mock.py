import asyncio
from typing import AsyncGenerator, List, Dict, Any, Optional
from .base import Backend

class MockBackend(Backend):
    """A mock backend for testing without external dependencies."""
    
    def name(self) -> str:
        return "mock"
        
    async def chat(
        self, 
        messages: List[Dict[str, str]], 
        tools: Optional[List[Dict[str, Any]]] = None
    ) -> AsyncGenerator[str, None]:
        response = "I am the Lumen AI Assistant. How can I help you today? (Note: This is a mock response)"
        
        for word in response.split():
            yield word + " "
            await asyncio.sleep(0.05)
