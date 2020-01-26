import sys
from engineio.async_drivers import gevent

import json
import os 

from auto_everything.base import IO
io = IO()

from flask import Flask, render_template,redirect
from flask_socketio import SocketIO, emit

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)
    
# make sure static folder is the react build folder, and static path is the root, so static_url_path = ''
app = Flask(__name__, template_folder=resource_path('./front-end_app/build'), static_url_path='', static_folder=resource_path('./front-end_app/build'))
app.config['SECRET_KEY'] = 'yingshaoxo is the king'
socketio = SocketIO(app, cors_allowed_origins='*')

msgs = []
#data_folder = os.path.expanduser("~/.mathchat")
data_folder = "/root/mathchat"
temp_json_file = os.path.join(data_folder, "msgs.json")
if not os.path.exists(data_folder):
    os.mkdir(data_folder)
if not os.path.exists(temp_json_file):
    io.write(temp_json_file, json.dumps([]))

@app.route('/')
def index():
    return render_template('index.html')

@app.errorhandler(404)
def page_not_found(e):
    print(e)
    return redirect("/")

@socketio.on("you have total control about this text for identifying tunnel name")
def handle_data(message):
    global msgs
    msgs = json.loads(io.read(temp_json_file))

    emit('you have total control about this text for identifying tunnel name', json.dumps(msgs)) # send historical msgs to new connector

@socketio.on('message_receiver_on_server')
def handle_data(message): # data could be anything, json or text
    print(message)

    global msgs
    msgs.append(json.loads(message))
    msgs = msgs[-10:]
    io.write(temp_json_file, json.dumps(msgs))

    emit('message_receiver_on_client', message, broadcast=True, include_self=False) # when broadcast=True, it'll send a message to everyone except current socket

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=True)
