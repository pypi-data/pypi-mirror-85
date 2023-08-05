#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 19 14:51:52 2017

@author: Michael Blahay

Created this because there is no good way use common unix utilities to crop a file
down to some portion of the middle. In particular, there isn't a good way to remove
a specified number of lines from the end of a file without first knowing the number
of lines in the file. Though, this can be done, it would require multiple passes
through a file. For a stream, multiple passes would be impossible unless the stream
is first saved to a file, which may not be reasonable depending on the size of the 
stream.
"""

import sys
import argparse
import logging
from collections import deque

def body(iterobject, head=0, tail=0):
    'This is the method where the magic happens. The method is a generator that will process through an interable and output the desired elements.'
    
    lg = logging.getLogger(__name__)
    lg.debug('Entering into generator head = %s, tail = %s', head, tail)
    
    rn = 0 #variable for tracking record number

    cache = deque()  #initializing the cache. The cache is what allow us to crop at the end of the file
    lg.debug('Beginning iteration')
    
    for l in iterobject:     #Please note that the more there is to be removed from the end of the file, the larger the cache, and the larger the cache, the more memory is consumed.
        lg.debug("l = %s", l)
        rn+=1
        lg.debug('rn = %s', rn)    
        if rn > head:
            cache.append(l)
            lg.debug('cache = %s',cache)

        if rn > head + tail:
            yield cache.popleft()

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

if __name__ == '__main__':
    # Setting up the logging environment for individual execution.
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
        
