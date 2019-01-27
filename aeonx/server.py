import asyncio
import websockets
import json
import time
import os

async def boot(websocket, path):
    print("connected client")
    try:
        await handleClient(websocket)
    except websockets.exceptions.ConnectionClosed:
        print("connection closed")


async def handleClient(websocket):
    async for message in websocket:
        print(message)
    

start_server = websockets.serve(boot, '10.0.0.8', port=8000)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()

