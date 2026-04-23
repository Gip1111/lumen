import aiohttp
import json
from typing import AsyncGenerator, List, Dict, Any, Optional
from .base import Backend

class OllamaBackend(Backend):
    """Backend for local Ollama instance."""
    
    def __init__(self, host: str = "http://localhost:11434", model: str = "llama3"):
        self.host = host
        self.model = model
        
    def name(self) -> str:
        return f"ollama ({self.model})"
        
    async def chat(
        self, 
        messages: List[Dict[str, str]], 
        tools: Optional[List[Dict[str, Any]]] = None
    ) -> AsyncGenerator[str, None]:
        url = f"{self.host}/api/chat"
        payload = {
            "model": self.model,
            "messages": messages,
            "stream": True
        }
        
        if tools:
            payload["tools"] = tools

        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(url, json=payload) as response:
                    async for line in response.content:
                        if line:
                            chunk = json.loads(line)
                            if "message" in chunk and "content" in chunk["message"]:
                                yield chunk["message"]["content"]
                            if chunk.get("done"):
                                break
            except Exception as e:
                yield f"Error connecting to Ollama: {e}"
