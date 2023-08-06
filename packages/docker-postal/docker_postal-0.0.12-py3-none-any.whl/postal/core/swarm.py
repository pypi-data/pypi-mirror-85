import os
from . import config
from .utils import shell

def proxy(args):
    return shell(f'docker {" ".join(args)}')

def deploy(stack, dir=None, branch=None):
    if dir:
        compose = 'stack/production.yml'
        with open(os.path.join(dir, 'stack/production.env'), 'w') as f:
            env = config.all(stack)
            for key in env:
                f.write(f'{key}={env[key]}\n')
        shell(f'cd {dir} && docker-compose -p {stack} -f {compose} build')
        shell(f'cd {dir} && docker-compose -p {stack} -f {compose} push')
        shell(f'cd {dir} && docker stack deploy --with-registry-auth -c {compose} {stack}')
        shell(f'rm -rf {dir}', silent=True)
    else:
        raise Exception("Deploying from github is not yet implemented.")
        # shell('git clone')
