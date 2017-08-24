import asyncio
import websockets


connected = set()


async def my_function(websocket, msg):
    print(msg)
    for ws in connected:
        if ws != websocket:
            try:
                await ws.send(msg)
            except:
                # Unregister
                connected.remove(ws)


async def main_handler(websocket, path):
    # Register
    global connected
    connected.add(websocket)

    while True:
        try:
            msg = await websocket.recv()
            await my_function(websocket, msg)
        except:
            pass


start_server = websockets.serve(main_handler, '0.0.0.0', 5678)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()