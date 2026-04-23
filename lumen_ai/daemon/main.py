import asyncio
import json
import logging
import os
import sys
import aiohttp
from typing import Dict, Any

from lumen_ai.backends.mock import MockBackend
from lumen_ai.tools.manager import registry
from lumen_ai.daemon.persistence import PersistenceManager
import lumen_ai.tools.system # Ensure tools are registered

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stdout
)
logger = logging.getLogger("lumen-aid")

SOCKET_PATH = os.environ.get("XDG_RUNTIME_DIR", "/tmp") + "/lumen-aid.sock"

class JsonRpcServer:
    def __init__(self, backend):
        self.backend = backend

    async def handle_request(self, reader, writer):
        addr = writer.get_extra_info('peername')
        logger.info(f"New connection from {addr or 'client'}")

        try:
            while True:
                # Limit line size to 1MB to prevent DOS
                line = await reader.readline()
                if not line or len(line) > 1024 * 1024:
                    if len(line) > 1024 * 1024:
                        logger.warning("Request too large, closing connection.")
                    break
                
                try:
                    request = json.loads(line)
                    logger.debug(f"Received request: {request}")
                    
                    method = request.get("method")
                    params = request.get("params", {})
                    request_id = request.get("id")

                    if method == "chat":
                        await self.handle_chat(params, request_id, writer)
                    elif method == "get_tools":
                        await self.send_response({"id": request_id, "result": registry.get_tool_definitions()}, writer)
                    else:
                        await self.send_error(request_id, -32601, "Method not found", writer)

                except json.JSONDecodeError:
                    await self.send_error(None, -32700, "Parse error", writer)
        
        except Exception as e:
            logger.error(f"Error handling request: {e}")
        finally:
            writer.close()
            await writer.wait_closed()

    async def handle_chat(self, params, request_id, writer):
        messages = params.get("messages", [])
        
        # In a more advanced implementation, we would use LLM function calling
        # For this foundation, we simulate the flow:
        # 1. Stream the AI response
        # 2. Check if a tool call is triggered (simulated or real)
        
        async for token in self.backend.chat(messages):
            await self.send_notification("chat_token", {"id": request_id, "token": token}, writer)
            
        # Example: check if the backend wants to call a tool
        # (This is where real tool-calling logic would go)
        
        await self.send_response({"id": request_id, "result": "done"}, writer)

    async def request_tool_confirmation(self, tool_name, args, writer):
        """Sends a confirmation request to the client and waits for approval."""
        confirm_id = os.urandom(4).hex()
        await self.send_notification("tool_confirmation_request", {
            "confirm_id": confirm_id,
            "tool_name": tool_name,
            "args": args
        }, writer)
        
        # In a real implementation, we would wait for a 'tool_response' request with this confirm_id
        # For now, we simulate the structure
        return True

    async def execute_tool(self, tool_name, args):
        """Executes a registered tool after validation."""
        if tool_name in registry.tools:
            tool_info = registry.tools[tool_name]
            # Here we would validate args against schema
            try:
                return await tool_info["func"](**args)
            except Exception as e:
                return {"error": str(e)}
        return {"error": "Tool not found"}

    async def send_response(self, data, writer):
        writer.write(json.dumps(data).encode() + b"\n")
        await writer.drain()

    async def send_notification(self, method, params, writer):
        notification = {"jsonrpc": "2.0", "method": method, "params": params}
        await self.send_response(notification, writer)

    async def send_error(self, request_id, code, message, writer):
        error = {"jsonrpc": "2.0", "id": request_id, "error": {"code": code, "message": message}}
        await self.send_response(error, writer)

async def run_daemon():
    logger.info("Starting Lumen AI Daemon (lumen-aid)...")
    
    # Cleanup old socket
    if os.path.exists(SOCKET_PATH):
        os.remove(SOCKET_PATH)

    # Backend selection logic
    from lumen_ai.backends.ollama import OllamaBackend
    
    backend = OllamaBackend()
    # Check if Ollama is reachable, otherwise fallback
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get("http://localhost:11434/api/tags") as resp:
                if resp.status == 200:
                    logger.info("Connected to local Ollama instance.")
                else:
                    raise Exception("Ollama not responding correctly")
    except Exception:
        logger.warning("Ollama not found. Falling back to MockBackend.")
        backend = MockBackend()

    # Import driver tools to register them
    import lumen_ai.tools.drivers
    
    # Initialize persistence
    persistence = PersistenceManager()
    
    server = JsonRpcServer(backend)
    server.persistence = persistence

    try:
        srv = await asyncio.start_unix_server(server.handle_request, path=SOCKET_PATH)
        # Security: restrict socket access to the current user
        os.chmod(SOCKET_PATH, 0o600)
        logger.info(f"Listening on {SOCKET_PATH} (restricted permissions)")
        
        async with srv:
            await srv.serve_forever()
    except Exception as e:
        logger.error(f"Failed to start server: {e}")

def main():
    try:
        asyncio.run(run_daemon())
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    main()
