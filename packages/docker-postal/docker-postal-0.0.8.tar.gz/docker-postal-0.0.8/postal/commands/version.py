from postal.core.rpc import Proxy
from postal.version import version

help = "Proxy a docker command to swarm manager"

def arguments(parser):
    pass

def main(args=None):
    print(version)
