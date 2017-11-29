import env

from database import MySession
from security import Auth
s = MySession()
auth = Auth(s)

from flask import Flask, url_for, redirect, request, render_template, session
import json

msgs = []
app = Flask(__name__, static_url_path='', static_folder='', template_folder='templates')
    
@app.before_request
def session_management(): 
    session.permanent = True

@app.route('/')
def index():
    # return app.send_static_file('index.html')
    env.set()
    global msgs

    username = session.get('username')
    if username == None:
        return redirect(url_for('login'))
    else:
        new_msgs = msgs.copy()
        for msg in new_msgs:
            if msg['name'] == username:
                msg['side'] = 'right'
            else:
                msg['side'] = 'left'

        response = app.make_response(render_template('index.html', msgs=new_msgs))
        token = auth.set_token(username)
        if token == None: 
            return redirect(url_for('login'))
        response.set_cookie('token', value=token)
        response.set_cookie('username', value=username)
        return response

@app.errorhandler(404)
def page_not_found(e):
    return redirect('/')

@app.route('/msg/', methods=['POST'])
def get_msg():
    if request.method == 'POST':
        global msgs # using global to tell this function there already have msgs var, no need to set a new one, it's important in this situation.
        content = request.data.decode('utf-8')
        msg_dict = json.loads(content)
        msgs.append(msg_dict)
        msgs = msgs[-12:]
        return ''

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if request.form['btn'] == 'Log in/up':
            if username.strip(' ') != '' and password.strip(' ') != '':
                user = s.find_one(username)
                if user != None:
                    if user.password != password:
                        error = 'Password wrong'
                    else:
                        # Logged in
                        session['username'] = username
                        return redirect(url_for('index'))
                else:
                    s.add(username, password)
                    s.commit()
                    # logged up
                    session['username'] = username
                    return redirect(url_for('index'))
                    
            else:
                error = "Do not leave a blank on username or password!"
    return render_template('login.html', error=error)

if __name__ == '__main__':
    app.secret_key = "Every day is a different day."
    app.run(host='0.0.0.0', port=5000, debug=True)
