import asyncio
import websockets
import json
import time
import os

async def boot(websocket, path):
    print("connected client")
    try:
        await handleClient(client)
    except websockets.exceptions.ConnectionClosed:
        print("connection closed")


async def handleClient(client):
    async for message in client.websocket:
        print(message)
    

start_server = websockets.serve(boot, port=8000)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()

