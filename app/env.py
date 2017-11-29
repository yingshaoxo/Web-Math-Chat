import os
import sys
import shlex, subprocess

version = sys.version_info 

def run_command(c):
    args_list = shlex.split(c)
    result = subprocess.run(args_list, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True, timeout=15)
    return str(result.stdout)

def run_program(name):
    args_list = shlex.split(name)
    p = subprocess.Popen(args_list)
    
def set():
    current_dir = os.path.abspath(os.path.dirname(__file__))
    server_path = os.path.join(current_dir, 'server.py')
    if 'app/server.py' not in run_command('ps x'):
        run_program('python{major}.{minor} {path} &'.format(major=str(version[0]), minor=str(version[1]), path=server_path))

# set()
