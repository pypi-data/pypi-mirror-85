from pydantic import BaseModel
from typing import Dict
from fastapi import WebSocket


class SocketMessage(BaseModel):
    """
    SocketMessage represents the action and data that is passed in and passed out of a socket connection
    """
    action: str
    data: dict = {}


class SocketConnectionManager:
    """
    SocketConnectionManager manaqges a bunch of socket connections
    """
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}

    """
    Call when a new SocketConnection is connected
    
    MUST BE AWAITED
    """
    async def connect(self, identifier: str, websocket: WebSocket):
        await websocket.accept()
        self.active_connections[identifier] = websocket

    """
    Call when a new SocketConnection is disconnected
    """
    def disconnect(self, identifier: str):
        del self.active_connections[identifier]

    """
    Get the websocket connection that corresponds to an identifier
    """
    def get_connection(self, identifier: str) -> WebSocket:
        return self.active_connections[identifier]

    """
    Get the identifier that corresponds to a websocket connection
    """
    def get_participant(self, websocket: WebSocket) -> str:
        for identifier, connection in self.active_connections:
            if connection == websocket:
                return identifier

    """
    Sends a new websocket message to a identifier's socket connection
    
    MUST BE AWAITED
    """
    async def send(self, message: SocketMessage, identifier: str):
        await self.get_connection(identifier).send_text(message.json())

    """
    Broadcast a new websocket message to all connected connections managed by this object

    MUST BE AWAITED
    """
    async def broadcast(self, message: SocketMessage):
        for connection in self.active_connections.values():
            await connection.send_text(message.json())
