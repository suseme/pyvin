__author__ = 'vin@misday.com'

import Queue
import threading
import time
from .callbacks import Callbacks
from .log import Log

class Processor(threading.Thread, Callbacks):
    (EVT_START, EVT_STOP, EVT_LOOP) = range(1, 4)

    def __init__(self, interval = 0):
        threading.Thread.__init__(self)
        Callbacks.__init__(self)
        self.init([Processor.EVT_START, Processor.EVT_STOP, Processor.EVT_LOOP])

        self.interval = interval

        print 'Processor init...'

    def run(self):
        print 'Processor start...'
        self.running = True

        willLoop = self.dispatch(Processor.EVT_START) #self.handler.onStart()

        while self.running and willLoop:
            willLoop = self.dispatch(Processor.EVT_LOOP) # self.handler.onLoop()
            if self.interval > 0:
                time.sleep(self.interval)

        self.dispatch(Processor.EVT_STOP) # self.handler.onStop()
        print 'Processor stop...'

    def stop(self):
        self.running = False

    ###############################################################
    def initMsgQ(self):
        self.queue = Queue.Queue()

    def recvMsg(self, block=True, timeout=None):
        try:
            msg = self.queue.get(block, timeout)
        except:
            msg = None
            # Log.e(Processor.__name__, 'recv msg failed')
        return msg

    def sendMsgTo(self, msg):
        self.queue.put(msg)