from flask import Flask, redirect, request, render_template
import json

global msgs 
msgs = []
app = Flask(__name__, static_url_path='', static_folder='', template_folder='')

@app.route('/')
def index():
    # return app.send_static_file('index.html')
    global msgs
    return render_template('index.html', msgs=msgs)

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
        msgs = msgs[-10:]
        return ''

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
