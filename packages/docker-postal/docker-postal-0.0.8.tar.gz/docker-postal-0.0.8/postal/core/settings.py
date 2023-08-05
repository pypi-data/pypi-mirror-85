import os
import json
from pathlib import Path
from appdirs import user_config_dir


config_dir = user_config_dir('postal')
config_path = os.path.join(config_dir, 'config.json')

def set(**kwargs):
    Path(config_dir).mkdir(parents=True, exist_ok=True)
    config = get()
    with open(config_path, 'w') as f:
        f.write(json.dumps({**config, **kwargs}, indent=4))

def get():
    try:
        with open(config_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
