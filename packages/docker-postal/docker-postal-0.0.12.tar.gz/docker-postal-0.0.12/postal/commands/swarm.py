from postal.core.rpc import Proxy


help = "Proxy a docker command to swarm manager"

def arguments(parser):
    pass

def main(args=None):
    Proxy().swarm_proxy(args.remainder)
