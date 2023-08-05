import pkgutil
import os
from astropy.io import ascii
import esopipeline as root

def load_table(ins, name):
    package = root.__package__
    data = pkgutil.get_data(package, '/'.join(('templates', ins, name)))
    text = data.decode()
    tab = ascii.read(text, format='fixed_width_two_line')
    return tab

def get_template_dir():
    return os.path.join(root.__path__[0], 'templates')

def list_instruments():
    path = get_template_dir()
    instruments = os.listdir(path)
    return instruments 

def listdir(dir, test=lambda x: True, path=False):
    files = [f for f in os.listdir(dir) if test(os.path.join(dir, f))]
    return files

def list_workflows(ins, include_default=False):
    path = os.path.join(get_template_dir(), ins)
    workflows = listdir(path, test=os.path.isdir)
    if not include_default:
        workflows = [w for w in workflows if w != 'default']
    return workflows

def get_default_workflow(ins):
    filename =  os.path.join(get_template_dir(), ins, 'default')
    workflow = os.readlink(filename)
    return workflow

