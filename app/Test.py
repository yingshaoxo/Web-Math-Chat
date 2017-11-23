from database import MySession
from pprint import pprint

s = MySession()

'''
r = s.find_one(id='yingshaoxo', password='123')
r.token = 'dddd'

pprint(r.token)
'''

'''
def func1(*args, **kwargs):
    return args, kwargs

def func2(*args, **kwargs):
    return args, kwargs

a, b = func1(id='yingshaoxo', password='123')
print(func2(*a, **b))
'''

from security import Auth

auth = Auth(s)
print(auth.set_token('yingshaoxo'))


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

