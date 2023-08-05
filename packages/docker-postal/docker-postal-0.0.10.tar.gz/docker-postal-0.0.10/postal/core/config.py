import sys
import json
from postal.core import db


# get entire config as directory
def all(stack):
    return db.get(stack)

# set value
def set(stack, name, value):
    vars = db.get(stack)
    vars[name] = value
    db.set(stack, vars)

# get value
def get(stack, name):
    vars = db.get(stack)
    return vars.get(name)

# remove key
def rm(stack, name):
    vars = db.get(stack)
    vars.pop(name)
    db.set(stack, vars)

# load from stdin
def load(stack):
    vars = json.loads(sys.stdin.read())
    try:
        for key in vars: assert isinstance(vars[key], str)
    except (json.decoder.JSONDecodeError, AssertionError, TypeError) as exc:
        print(exc)
        print('Invalid format: config should be a json file with keys and values of type string.')
    db.set(stack, vars)

# dump to stdout
def dump(stack):
    vars = db.get(stack)
    return print(json.dumps(vars, indent=2))
