from flask import Flask, render_template
from flask_socketio import SocketIO, emit
    
# make sure static folder is the react build folder, and static path is the root, so static_url_path = ''
app = Flask(__name__, static_url_path='', static_folder='../front-end_app/build')
app.config['SECRET_KEY'] = 'yingshaoxo is the king'
socketio = SocketIO(app)

@socketio.on('my event')
def test_message(message):
    emit('my response', {'data': 'got it!'})

if __name__ == '__main__':
    socketio.run(app, debug=True)
