from flask import Flask, redirect

app = Flask(__name__, static_url_path='', static_folder='')

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.errorhandler(404)
def page_not_found(e):
    return redirect('/')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
