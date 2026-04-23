import json
import asyncio
import os
import threading
from PySide6.QtCore import QObject, Signal, Slot, Property, QAbstractListModel, Qt

class ChatModel(QAbstractListModel):
    RoleRole = Qt.UserRole + 1
    ContentRole = Qt.UserRole + 2

    def __init__(self, parent=None):
        super().__init__(parent)
        self._messages = []

    def rowCount(self, parent=None):
        return len(self._messages)

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid() or index.row() >= len(self._messages):
            return None
        message = self._messages[index.row()]
        if role == self.RoleRole:
            return message["role"]
        elif role == self.ContentRole:
            return message["content"]
        return None

    def roleNames(self):
        return {
            self.RoleRole: b"role",
            self.ContentRole: b"content"
        }

    def append_message(self, role, content):
        self.beginInsertRows(self.index(len(self._messages), 0), len(self._messages), len(self._messages))
        self._messages.append({"role": role, "content": content})
        self.endInsertRows()

    def update_last_message(self, content):
        if self._messages:
            self._messages[-1]["content"] += content
            self.dataChanged.emit(self.index(len(self._messages)-1, 0), self.index(len(self._messages)-1, 0))

class Bridge(QObject):
    querySent = Signal(str)
    responseReceived = Signal(str)

    def __init__(self, chat_model):
        super().__init__()
        self.chat_model = chat_model
        self.socket_path = os.environ.get("XDG_RUNTIME_DIR", "/tmp") + "/lumen-aid.sock"
        self.loop = asyncio.new_event_loop()
        self.thread = threading.Thread(target=self._run_event_loop, daemon=True)
        self.thread.start()

    def _run_event_loop(self):
        asyncio.set_event_loop(self.loop)
        self.loop.run_forever()

    @Slot(str)
    def sendQuery(self, text):
        self.chat_model.append_message("user", text)
        asyncio.run_coroutine_threadsafe(self._communicate(text), self.loop)

    async def _communicate(self, text):
        try:
            reader, writer = await asyncio.open_unix_connection(self.socket_path)
            
            # Send chat request
            request = {
                "jsonrpc": "2.0",
                "method": "chat",
                "params": {"messages": [{"role": "user", "content": text}]},
                "id": 1
            }
            writer.write(json.dumps(request).encode() + b"\n")
            await writer.drain()

            # First AI response entry
            self.chat_model.append_message("assistant", "")

            while True:
                line = await reader.readline()
                if not line:
                    break
                
                resp = json.loads(line)
                if resp.get("method") == "chat_token":
                    token = resp["params"]["token"]
                    self.chat_model.update_last_message(token)
                elif "result" in resp:
                    break

            writer.close()
            await writer.wait_closed()
        except Exception as e:
            self.chat_model.update_last_message(f"Error: {e}")
