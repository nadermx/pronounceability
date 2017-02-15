import sys
from rq import Worker, Connection

import utilities

if __name__ == '__main__':
    with Connection():
        qs = sys.argv[1:] or ['default']

        w = Worker(qs)
        w.work()


