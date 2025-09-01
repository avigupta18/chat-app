from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from typing import Dict, List
import json

from .crud import save_message

app = FastAPI()

# Store connections per room
active_connections: Dict[int, List[WebSocket]] = {}

async def connect(room_id: int, websocket: WebSocket):
    await websocket.accept()
    if room_id not in active_connections:
        active_connections[room_id] = []
    active_connections[room_id].append(websocket)

def disconnect(room_id: int, websocket: WebSocket):
    active_connections[room_id].remove(websocket)
    if not active_connections[room_id]:
        del active_connections[room_id]

async def broadcast(room_id: int, message: dict):
    if room_id in active_connections:
        for connection in active_connections[room_id]:
            await connection.send_text(json.dumps(message))

@app.websocket("/ws/chat/{room_id}")
async def websocket_endpoint(websocket: WebSocket, room_id: int):
    await connect(room_id, websocket)
    try:
        while True:
            data = await websocket.receive_text()
            payload = json.loads(data)

            sender = payload.get("sender")
            content = payload.get("message")

            # Save to DB
            msg = await save_message(room_id, sender, content)

            response = {
                "id": msg.id,
                "room_id": room_id,
                "sender": sender,
                "content": content,
                "timestamp": str(msg.timestamp),
            }

            # Broadcast to all in the room
            await broadcast(room_id, response)

    except WebSocketDisconnect:
        disconnect(room_id, websocket)
