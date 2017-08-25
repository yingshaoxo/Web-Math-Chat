from subprocess import Popen
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
Popen(['python', os.path.join(current_dir,'server.py')])
# Popen(['python', os.path.join(current_dir,'app.py')])

from app import app
app.run(host='0.0.0.0', debug=True)
