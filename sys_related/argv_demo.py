__author__ = 'dongdaqing'

import sys

class Demo(object):
    def __init__(self):
        pass

    def read_param(self):
        pass

if __name__ == '__main__':
    print len(sys.argv)
    print sys.argv[0]
    print sys.argv[1]
    print type(sys.argv[1])
    print sys.argv[2]
    print sys.argv[3]