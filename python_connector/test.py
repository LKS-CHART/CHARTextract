import django
import sys, json


def respond(message):
    if not type(message) == dict:
        message = {'message': message}
    print(json.dumps(message))
    sys.stdout.flush()


def save(**kwargs):
    respond({'function': 'save', 'params': kwargs})


respond({'status': 'Ready'})
sys.stdout.flush()
for line in sys.stdin:
    x = json.loads(line)
    respond(x['params'])
    globals()[x['function']](**x['params'])
    #print(json.dumps(json.loads(line)))
    sys.stdout.flush()