from pprint import pprint
from env import App

env = App()
print(env.run_command('uname -a'))



'''
import websockets
import asyncio
import json

async def hello():
    async with websockets.connect('ws://localhost:5678') as websocket:
        token = 'hi'
        data = json.dumps({'name':'yingshaoxo', 'token':token})
        await websocket.send(data)

        answer = await websocket.recv()
        print(answer)

asyncio.get_event_loop().run_until_complete(hello())
'''


