import os
import getpass
from postal.core.utils import shell


help = "Enter a container (using enter script if availiable.)"

def arguments(parser):
    parser.add_argument('container', type=str, help='container to enter')

def main(args):
    user = getpass.getuser()
    uid = os.geteuid()
    container = args.container
    bashable = shell(f'docker-compose -p {args.stack} -f {args.compose} exec {container} bash -c ls', silent=True)
    enterable = shell(f'docker-compose -p {args.stack} -f {args.compose} exec {container} ls /enter.sh', silent=True)
    shl = 'bash' if bashable else 'sh'
    if enterable:
        return shell(f'docker-compose -p {args.stack} -f {args.compose} exec {container} {shl} /enter.sh {user} {uid}')
    return shell(f'docker-compose -p {args.stack} -f {args.compose} exec {container} {shl}')
