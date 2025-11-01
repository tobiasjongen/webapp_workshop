import asyncio
from websockets.asyncio.client import connect
import json


async def hello():
    async with connect("ws://localhost:8765") as websocket: 
        initialMessages = await websocket.recv()
        print(initialMessages)

        while True:
            message = input("Enter Message: ")
            user = "console"
            jsonString = json.dumps({"user": user, "content": message})
            await websocket.send(jsonString)
            print(f"sent: '{jsonString}'")
            message = await websocket.recv()
            print(f"received: '{json.loads(message)}'")



if __name__ == "__main__":
    asyncio.run(hello())