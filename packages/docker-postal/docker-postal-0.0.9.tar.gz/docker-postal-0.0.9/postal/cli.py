import sys
from argparse import ArgumentParser
from . import commands
from .core import utils


def main():

    # parser
    help = ""
    description = 'A light Docker control tool designed around compose and swarm'
    parser = ArgumentParser(description=description)
    subparsers = parser.add_subparsers(help=help)

    # arguments
    pwd = utils.sanitized_working_directory()
    cmp = 'stack/development.yml' # on deploy commands overridden by production.yml
    parser.add_argument('-s', '--stack', type=str, default=pwd,
        help=f'stack name (pwd: {pwd})')
    parser.add_argument('-c', '--compose', type=str, default=cmp,
        help=f'compose file (stack/[development|production].yml)')

    # development commands
    commands.register(subparsers, 'launch', commands.launch)
    commands.register(subparsers, 'enter', commands.enter)
    commands.register(subparsers, 'up', commands.compose, help='Bring docker compose stack up')
    commands.register(subparsers, 'down', commands.compose, help='Bring docker compose stack down')
    commands.register(subparsers, 'logs', commands.compose, help='Show docker logs for compose stack')
    commands.register(subparsers, 'compose', commands.compose)

    # swarm commands
    commands.register(subparsers, 'config', commands.config)
    commands.register(subparsers, 'deploy', commands.deploy)
    commands.register(subparsers, 'swarm', commands.swarm)
    # commands.register(subparsers, 'remote', commands.remote)

    # management commands
    commands.register(subparsers, 'login', commands.login)
    commands.register(subparsers, 'call', commands.call)
    commands.register(subparsers, 'version', commands.version)

    # special fixes for compose and deploy proxy commands
    arguments = sys.argv[1:]
    remainder = arguments
    if len(arguments) > 0 and (arguments[0] == 'compose' or arguments[0] == 'swarm'):
        remainder = arguments[1:]   # everything after compose or deploy store in proxied
        arguments = arguments[:1]   # everything before store in arguments

    # parse args
    args = parser.parse_args(arguments)
    args.remainder = remainder

    # execute command
    try:
        if hasattr(args, 'cmd'):
            sys.exit(args.cmd(args))
        else:
            parser.print_help()
    except KeyboardInterrupt:
        print('')
        sys.exit()
