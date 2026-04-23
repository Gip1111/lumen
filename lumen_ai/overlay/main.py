import sys
import os
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine
from .bridge import Bridge, ChatModel

def main():
    app = QGuiApplication(sys.stdout)
    
    # Register ChatModel and Bridge
    chat_model = ChatModel()
    bridge = Bridge(chat_model)
    
    engine = QQmlApplicationEngine()
    
    # Expose objects to QML
    engine.rootContext().setContextProperty("chatModel", chat_model)
    engine.rootContext().setContextProperty("bridge", bridge)
    
    # Load Main.qml
    qml_file = os.path.join(os.path.dirname(__file__), "Main.qml")
    engine.load(qml_file)
    
    if not engine.rootObjects():
        sys.exit(-1)
        
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
