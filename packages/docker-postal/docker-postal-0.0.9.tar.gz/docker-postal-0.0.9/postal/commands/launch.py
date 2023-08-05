from postal.core.utils import shell
from .enter import main as enter

help = "Rebuild and restart stack"

def arguments(parser):
    parser.add_argument('-e', '--enter', type=str, help='container to enter after launch')

def main(args):
    shell(f'docker-compose -p {args.stack} -f {args.compose} down --remove-orphans')
    shell(f'docker-compose -p {args.stack} -f {args.compose} build')
    shell(f'docker-compose -p {args.stack} -f {args.compose} up -d --force-recreate')
    if hasattr(args, 'enter'):
        args.container = args.enter
        enter(args)
