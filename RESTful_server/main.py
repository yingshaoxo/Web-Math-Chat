import json

from flask import Flask, render_template
from flask_socketio import SocketIO, emit
    
# make sure static folder is the react build folder, and static path is the root, so static_url_path = ''
app = Flask(__name__, template_folder='../front-end_app/build', static_url_path='', static_folder='../front-end_app/build')
app.config['SECRET_KEY'] = 'yingshaoxo is the king'
socketio = SocketIO(app)

msgs = []

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on("you have total control about this text for identifying tunnel name")
def handle_data(message):
    global msgs
    msgs = msgs[-10:]
    print(message)
    emit('you have total control about this text for identifying tunnel name', json.dumps(msgs)) # send historical msgs to new connector

@socketio.on('message_receiver_on_server')
def handle_data(message): # data could be anything, json or text
    global msgs
    print(message)
    msgs.append(json.loads(message))
    emit('message_receiver_on_client', message, broadcast=True, include_self=False) # when broadcast=True, it'll send a message to everyone except current socket

if __name__ == '__main__':
    socketio.run(app, debug=True)
