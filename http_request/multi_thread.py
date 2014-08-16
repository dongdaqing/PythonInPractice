__author__ = 'dongdaqing'

import threading,time
class MyThread(threading.Thread):
    def __init__(self, name=None):
        threading.Thread.__init__(self)
        self.name = name

    def run(self):
        print time.strftime('%Y-%m-%d %H-%M-%S',time.localtime())
        print self.name

def test():
    for i in range(0, 100):
        t = MyThread("thread_" + str(i))
        t.start()

if __name__=='__main__':
    test()