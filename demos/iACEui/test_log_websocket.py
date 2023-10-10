import asyncio
import websockets

async def hello():
    uri = "ws://localhost:8000/logs"
    async with websockets.connect(uri) as ws:
        greeting = await ws.recv()
        print(f"< {greeting}")

asyncio.get_event_loop().run_until_complete(hello())
