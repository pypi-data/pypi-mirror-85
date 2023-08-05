import sys
from postal.core.utils import shell


help = "Proxy a docker compose command with configured compose file selected"

def arguments(parser):
    pass

def main(args=None):
    sys.exit(shell(f'docker-compose -p {args.stack} -f {args.compose} {" ".join(args.remainder)}'))
