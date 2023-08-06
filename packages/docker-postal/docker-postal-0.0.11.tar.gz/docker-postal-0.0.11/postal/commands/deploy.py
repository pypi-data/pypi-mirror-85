import os
import sys
from postal.core.rpc import Proxy


help = "Deploy stack from origin repository or working dir"

def arguments(parser):
    parser.add_argument('-b', '--branch', type=str, help='deploy specific branch from origin')
    parser.add_argument('-w', '--working', action='store_true', help='deploy working directory')
    parser.add_argument('-y', '--yes', action='store_true', help='skip confirmation dialog')

def main(args=None):
    confirmation = f"Please enter stack name '{args.stack}' to confirm: "
    if not args.yes and input(confirmation).strip() != args.stack:
        print('Deploy cancelled.')
        sys.exit(1)
    proxy = Proxy()
    if args.working:
        destination = proxy.send(os.getcwd())
        proxy.swarm_deploy(stack=args.stack, dir=destination)
    else:
        raise Exception("Deploying from github is not yet implemented.")
