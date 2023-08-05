import sys
import argparse
import logging
from collections import deque

from .body import body


def initializeLogger():
    '''
    This function simply contains an encapsolation of the logger setup.
    The code was refactored from the main execution.
    '''
    lg = logging.getLogger(__name__)
    hd = logging.StreamHandler()
    hd.setLevel(logging.DEBUG)
    hd.setFormatter(logging.Formatter('%(asctime)s  %(levelname)s: %(message)s'))
    lg.addHandler(hd)
    return lg



lg = initializeLogger()

'Anything within this if construct represents the program that is called when crop is used within the context of a command line'
parser = argparse.ArgumentParser(add_help=False)
parser.add_argument('-?', '--help', action='help', default=argparse.SUPPRESS, help="Show this help message and exit.")
parser.add_argument("-h","--head",default="0",help="Number of head records to crop")
parser.add_argument("-t","--tail",default="0",help="Number of tail records to crop")
parser.add_argument("-d","--debug",action="store_true",help="Activate debug output")
parser.add_argument("filename",default="-", nargs="?",help="File to read intput from, if '-', then read from standard input")
args=parser.parse_args()

if args.debug: lg.setLevel(logging.DEBUG) # This actually sets the output level at the logger layer. This is important because this is the entry 
                                            # point layer for the logger and provides the best performance benefit when there is a need to exclude 
                                            # logging levels.

if args.filename == "-":
    f = sys.stdin
else:    
    f = open(args.filename)

h = int(args.head)
t = int(args.tail)
d = args.debug

try:
    for i in body(f,h,t):
        sys.stdout.write(i)

except IOError:
    raise
finally:
    f.close() # Make sure that the file is closed.
    sys.stdout.flush() # Flush the output buffer to make sure it is clear before exit
    
