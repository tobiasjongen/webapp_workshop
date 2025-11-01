from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import json
from datetime import datetime

app = FastAPI(title="Simple Messenger API")

# Add CORS middleware to allow frontend to communicate with backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

messages = []

class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        try:
            self.active_connections.remove(websocket)
        except ValueError:
            pass

    async def broadcast(self, message: str):
        to_remove = []
        for connection in list(self.active_connections):
            try:
                await connection.send_text(message)
            except Exception:
                to_remove.append(connection)
        for c in to_remove:
            self.disconnect(c)


manager = ConnectionManager()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """Simple WebSocket endpoint. Clients should send JSON messages.

    Supported client->server message shapes (JSON):
      {"type":"send_message","username":"alice","content":"hello"}

    Server->client messages (JSON):
      {"type":"new_message","message": { id, username, content, timestamp }}
    """
    await manager.connect(websocket)
    try:
        # Send initial sync of existing messages
        await websocket.send_text(json.dumps({"type": "init_sync", "messages": messages}))

        while True:
            data = await websocket.receive_text()
            try:
                payload = json.loads(data)
            except Exception:
                continue

            if payload.get("type") == "send_message":
                username = payload.get("username")
                content = payload.get("content")
                if not username or not content:
                    continue

                new_message = {
                    "id": len(messages) + 1,
                    "username": username.strip(),
                    "content": content.strip(),
                    "timestamp": __import__('datetime').datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                messages.append(new_message)
                # Broadcast to all connected clients
                await manager.broadcast(json.dumps({"type": "new_message", "message": new_message}))
            else:
                continue

    except WebSocketDisconnect:
        manager.disconnect(websocket)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
    