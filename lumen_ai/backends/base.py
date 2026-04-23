from abc import ABC, abstractmethod
from typing import AsyncGenerator, List, Dict, Any, Optional

class Backend(ABC):
    """Abstract base class for LLM backends."""
    
    @abstractmethod
    async def chat(
        self, 
        messages: List[Dict[str, str]], 
        tools: Optional[List[Dict[str, Any]]] = None
    ) -> AsyncGenerator[str, None]:
        """
        Sends a conversation history to the LLM and streams the response.
        
        Args:
            messages: List of message objects (role/content).
            tools: List of tool definitions available for the LLM.
            
        Yields:
            Token-by-token response strings.
        """
        pass

    @abstractmethod
    def name(self) -> str:
        """Returns the name of the backend."""
        pass
