import asyncio
import websockets

import requests
import json

from database import MySession
from security import Auth
s = MySession()
auth = Auth(s)

connected = dict()

async def my_function(websocket, data):
    # print(data)
    user = json.loads(data)

    my_struct = connected[websocket]
    if my_struct['verified'] == False:
        # print(auth.get_token(user['name']), '\n', user['token'])
        if auth.get_token(user['name']) != user['token']:
            websocket.handler_task.cancel()
        else:
            my_struct['verified'] = True
            return

    requests.post('http://0.0.0.0:5000/msg/', json={'name': user.get('name'), 'text': user.get('text')}) # /msg/ is diffrent one than /msg

    for ws in connected.copy().keys():
        if ws != websocket:
            try:
                await ws.send(data)
            except:
                # Unregister
                connected.pop(ws)
                my_struct['verified'] = False


async def main_handler(websocket, path):
    # Register
    global connected
    connected.update({websocket:{'username': None, 'verified': False}})

    while True:
        try:
            data = await websocket.recv()
            await my_function(websocket, data)
        except RuntimeError as e:
            print(e)

start_server = websockets.serve(main_handler, '0.0.0.0', 5678)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
