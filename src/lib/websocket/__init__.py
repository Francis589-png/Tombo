"""
TOMBO WebSocket Library - Real-time bidirectional communication
WebSocket server and client with events, rooms, and broadcasting.
"""

import json
import time
from typing import Dict, List, Callable, Any, Optional, Set


class WebSocketMessage:
    """WebSocket message."""
    
    def __init__(self, msg_type: str, data: Any, sender: str = None, room: str = None):
        """Initialize message.
        
        Args:
            msg_type: Message type (connect, disconnect, message, error)
            data: Message data
            sender: Sender identifier
            room: Room identifier
        """
        self.type = msg_type
        self.data = data
        self.sender = sender
        self.room = room
        self.timestamp = time.time()
    
    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            "type": self.type,
            "data": self.data,
            "sender": self.sender,
            "room": self.room,
            "timestamp": self.timestamp
        }
    
    def to_json(self) -> str:
        """Convert to JSON string."""
        return json.dumps(self.to_dict())
    
    @classmethod
    def from_json(cls, json_str: str) -> 'WebSocketMessage':
        """Create from JSON string."""
        data = json.loads(json_str)
        return cls(
            msg_type=data.get("type"),
            data=data.get("data"),
            sender=data.get("sender"),
            room=data.get("room")
        )


class WebSocketClient:
    """WebSocket client connection."""
    
    def __init__(self, client_id: str, send_handler: Callable):
        """Initialize client.
        
        Args:
            client_id: Unique client identifier
            send_handler: Function to send messages
        """
        self.id = client_id
        self.send_handler = send_handler
        self.rooms: Set[str] = set()
        self.metadata: Dict = {}
        self.connected_at = time.time()
        self.last_message_at = None
    
    def send(self, msg: WebSocketMessage):
        """Send message to client."""
        self.send_handler(msg)
    
    def join_room(self, room: str):
        """Join a room."""
        self.rooms.add(room)
    
    def leave_room(self, room: str):
        """Leave a room."""
        self.rooms.discard(room)
    
    def in_room(self, room: str) -> bool:
        """Check if in room."""
        return room in self.rooms
    
    def update_activity(self):
        """Update last activity timestamp."""
        self.last_message_at = time.time()


class WebSocketServer:
    """WebSocket server with rooms and broadcasting."""
    
    def __init__(self):
        """Initialize server."""
        self.clients: Dict[str, WebSocketClient] = {}
        self.rooms: Dict[str, Set[str]] = {}
        self.event_handlers: Dict[str, List[Callable]] = {}
        self.message_history: List[WebSocketMessage] = []
        self.max_history = 100
    
    def register_client(self, client_id: str, send_handler: Callable) -> WebSocketClient:
        """Register new client.
        
        Args:
            client_id: Unique client ID
            send_handler: Function to send messages
            
        Returns:
            WebSocketClient instance
        """
        client = WebSocketClient(client_id, send_handler)
        self.clients[client_id] = client
        
        # Broadcast connection event
        msg = WebSocketMessage("connect", {"client_id": client_id}, client_id)
        self._emit("connect", msg)
        
        return client
    
    def unregister_client(self, client_id: str):
        """Unregister client.
        
        Args:
            client_id: Client ID to remove
        """
        if client_id not in self.clients:
            return
        
        client = self.clients[client_id]
        
        # Leave all rooms
        for room in list(client.rooms):
            self.leave_room(client_id, room)
        
        # Broadcast disconnection
        msg = WebSocketMessage("disconnect", {"client_id": client_id}, client_id)
        self._emit("disconnect", msg)
        
        del self.clients[client_id]
    
    def create_room(self, room_name: str):
        """Create room."""
        self.rooms[room_name] = set()
    
    def join_room(self, client_id: str, room_name: str):
        """Add client to room.
        
        Args:
            client_id: Client ID
            room_name: Room name
        """
        if room_name not in self.rooms:
            self.create_room(room_name)
        
        if client_id in self.clients:
            self.clients[client_id].join_room(room_name)
            self.rooms[room_name].add(client_id)
            
            msg = WebSocketMessage(
                "room_join",
                {"client_id": client_id, "room": room_name},
                client_id,
                room_name
            )
            self._emit("room_join", msg)
    
    def leave_room(self, client_id: str, room_name: str):
        """Remove client from room.
        
        Args:
            client_id: Client ID
            room_name: Room name
        """
        if client_id in self.clients:
            self.clients[client_id].leave_room(room_name)
        
        if room_name in self.rooms:
            self.rooms[room_name].discard(client_id)
            
            msg = WebSocketMessage(
                "room_leave",
                {"client_id": client_id, "room": room_name},
                client_id,
                room_name
            )
            self._emit("room_leave", msg)
    
    def broadcast(self, msg: WebSocketMessage):
        """Broadcast message to all clients.
        
        Args:
            msg: Message to broadcast
        """
        for client in self.clients.values():
            client.send(msg)
        
        self._add_to_history(msg)
    
    def broadcast_to_room(self, room_name: str, msg: WebSocketMessage):
        """Broadcast message to room.
        
        Args:
            room_name: Room name
            msg: Message to broadcast
        """
        if room_name not in self.rooms:
            return
        
        for client_id in self.rooms[room_name]:
            if client_id in self.clients:
                self.clients[client_id].send(msg)
        
        msg.room = room_name
        self._add_to_history(msg)
    
    def send_to_client(self, client_id: str, msg: WebSocketMessage):
        """Send message to specific client.
        
        Args:
            client_id: Target client ID
            msg: Message to send
        """
        if client_id in self.clients:
            self.clients[client_id].send(msg)
    
    def handle_message(self, client_id: str, msg: WebSocketMessage):
        """Handle incoming message.
        
        Args:
            client_id: Sender client ID
            msg: Received message
        """
        msg.sender = client_id
        self.clients[client_id].update_activity()
        
        self._add_to_history(msg)
        self._emit("message", msg)
    
    def on(self, event: str, handler: Callable):
        """Register event handler.
        
        Args:
            event: Event name
            handler: Handler function
        """
        if event not in self.event_handlers:
            self.event_handlers[event] = []
        
        self.event_handlers[event].append(handler)
    
    def off(self, event: str, handler: Callable):
        """Unregister event handler.
        
        Args:
            event: Event name
            handler: Handler function
        """
        if event in self.event_handlers:
            self.event_handlers[event].remove(handler)
    
    def _emit(self, event: str, msg: WebSocketMessage):
        """Emit event to handlers."""
        if event in self.event_handlers:
            for handler in self.event_handlers[event]:
                try:
                    handler(msg)
                except Exception as e:
                    print(f"Event handler error: {e}")
    
    def _add_to_history(self, msg: WebSocketMessage):
        """Add message to history."""
        self.message_history.append(msg)
        if len(self.message_history) > self.max_history:
            self.message_history.pop(0)
    
    def get_clients_in_room(self, room_name: str) -> List[str]:
        """Get client IDs in room."""
        return list(self.rooms.get(room_name, set()))
    
    def get_room_list(self) -> List[str]:
        """Get all room names."""
        return list(self.rooms.keys())
    
    def get_client_rooms(self, client_id: str) -> List[str]:
        """Get rooms for client."""
        if client_id not in self.clients:
            return []
        return list(self.clients[client_id].rooms)
    
    def get_stats(self) -> Dict:
        """Get server statistics."""
        return {
            "total_clients": len(self.clients),
            "total_rooms": len(self.rooms),
            "total_messages": len(self.message_history),
            "rooms": {
                name: len(clients)
                for name, clients in self.rooms.items()
            }
        }


class WebSocketHandler:
    """Helper for managing WebSocket connections."""
    
    def __init__(self, server: WebSocketServer):
        """Initialize handler.
        
        Args:
            server: WebSocketServer instance
        """
        self.server = server
    
    def connect(self, client_id: str, send_fn: Callable):
        """Handle client connection."""
        return self.server.register_client(client_id, send_fn)
    
    def disconnect(self, client_id: str):
        """Handle client disconnection."""
        self.server.unregister_client(client_id)
    
    def receive(self, client_id: str, json_data: str):
        """Handle message receive."""
        try:
            msg = WebSocketMessage.from_json(json_data)
            self.server.handle_message(client_id, msg)
        except Exception as e:
            error_msg = WebSocketMessage("error", {"error": str(e)})
            self.server.send_to_client(client_id, error_msg)


def create_server() -> WebSocketServer:
    """Create new WebSocket server."""
    return WebSocketServer()
