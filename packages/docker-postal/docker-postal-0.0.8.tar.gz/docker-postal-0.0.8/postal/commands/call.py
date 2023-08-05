from postal.core.rpc import call


help = "Run rpc function on build and management server"


async def count(value, update=None):
    for v in range(value):
        await update(v)
    return value

def ping():
    return True

def arguments(parser):
    parser.add_argument('cid', type=str, help='call id is to pass input and output via a tmp file')

def main(args=None):
    call(args.cid)
