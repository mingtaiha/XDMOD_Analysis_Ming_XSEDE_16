import sys
import signal
import numpy as np

SIZE = 10000

def handler(signum, frame):
    print "Signal handler called with signal", signum
    sys.exit()

time = int(sys.argv[1]) * 60
signal.signal(signal.SIGALRM, handler)
signal.alarm(time)


while 1:
    A = np.random.rand(SIZE, SIZE)
    B = np.random.rand(SIZE, SIZE)
    C = A * B
