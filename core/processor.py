__author__ = 'vin@misday.com'

import threading, Queue, time, logging
from .callbacks import Callbacks

class Processor(threading.Thread, Callbacks):
    (EVT_START, EVT_STOP, EVT_LOOP, EVT_MAX_NUM) = range(1, 5)

    def __init__(self, name = '', interval = 0, log=None):
        if log:
            self.log = log
        else:
            self.log = logging.getLogger(Processor.__name__)
        threading.Thread.__init__(self)
        if name:
            self.name = name
        Callbacks.__init__(self)
        self.init([Processor.EVT_START, Processor.EVT_STOP, Processor.EVT_LOOP])
        self.interval = interval
        self.log.info('%s init...' % self.name)

    def run(self):
        self.log.info('%s start...' % self.name)
        self.running = True

        willLoop = self.dispatch(Processor.EVT_START)
        while self.running and willLoop:
            willLoop = self.dispatch(Processor.EVT_LOOP)
            if self.interval > 0:
                time.sleep(self.interval)

        self.dispatch(Processor.EVT_STOP) # self.handler.onStop()
        self.log.info('%s stop...' % self.name)

    def stop(self):
        # print 'stopping %s ...' % self.name
        self.running = False

    ###############################################################
    def initMsgQ(self):
        self.queue = Queue.Queue()

    def recvMsg(self, block=True, timeout=None):
        try:
            msg = self.queue.get(block, timeout)
        except:
            msg = None
        return msg

    def sendMsgToSelf(self, msg):
        self.queue.put(msg)