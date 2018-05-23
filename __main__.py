import sys
import json
# Define after imports and globals
available_funcs = {}


def exposed_function(func):
    available_funcs[getattr(func,'__name__')] = func


'''
####
Expose certain functions that allow the following:
- Run classifier
- Change variable, datafiles/columns and labelfiles/columns
- 
####
'''
print(available_funcs)


# simple JSON echo script

def respond(message):
    if not type(message) == dict:
        message = {'message': message}
    print(json.dumps(message))
    sys.stdout.flush()


def run(**kwargs):
    respond({'function': 'run', 'params': kwargs})

def save(**kwargs):
    respond({'function': 'save', 'params': kwargs})


respond({'status': 'Ready'})
sys.stdout.flush()
for line in sys.stdin:
    respond("pyshell")
    x = json.loads(line)
    respond(x['params'])
    globals()[x['function']](**x['params'])
    #print(json.dumps(json.loads(line)))
    respond("-------")
    sys.stdout.flush()