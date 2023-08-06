try:
    from importlib import metadata
except ImportError: # for Python<3.8
    import importlib_metadata as metadata

help = "Show current postal version"

def arguments(parser):
    pass

def main(args=None):
    print(metadata.version('docker-postal'))
