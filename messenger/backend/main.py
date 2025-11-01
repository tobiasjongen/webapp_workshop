import asyncio
import websockets
from websockets.asyncio.server import broadcast, serve
import json
import time
from datetime import datetime

CLIENTS = set()

MESSAGES = []

async def handle(websocket):
    print(f"client '{websocket.remote_address}' connected")
    CLIENTS.add(websocket) # store client for later broadcasting

    
    await websocket.send(json.dumps(MESSAGES)) # send complete message history to client
    print(f"sending message history to client '{websocket.remote_address}'")

    try:
        # loop until client disconnects
        while True:
            rawMessage = await websocket.recv() # receive message

            try:
                # parse received message
                # message must be JSON object containing keys "user" and "content"
                jsonMessage = json.loads(rawMessage) 
                if not isinstance(jsonMessage, dict):
                    raise ValueError("Message is not a JSON object")
                user = jsonMessage["user"]
                content = jsonMessage["content"]
            except (json.JSONDecodeError, KeyError, ValueError) as e:
                # handle errors
                error_msg = f"Malformed message from {websocket.remote_address}: {e}"
                print(error_msg)
                continue

            timestamp = int(time.time())
            message = {"user": user, "content": content, "timestamp": timestamp}

            print(f"{datetime.fromtimestamp(timestamp)} - {user}: '{content}'")
            MESSAGES.append(message) # add message to message history

            broadcast(CLIENTS, json.dumps([message])) # broadcast new message to all clients

    except websockets.ConnectionClosedOK:
        print(f"Client {websocket.remote_address} disconnected normally.")
    except websockets.ConnectionClosedError as e:
        print(f"Client {websocket.remote_address} disconnected with error: {e}")
    finally:
        CLIENTS.remove(websocket) # remove disconnected client

async def main():
    PORT = 8765
    print(f"Server started: listening on {PORT}")
    async with serve(handle, "0.0.0.0", PORT) as server:
        await server.serve_forever()


if __name__ == "__main__":
    asyncio.run(main())
