__author__ = 'vin@misday.com'

class Callbacks():
    def __init__(self):
        self.handler = {}

    def init(self, events):
        for event in events:
            self.handler[event] = self.callback

    def callback(self, *pros, **attrs):
        pass

    def bind(self, event, handler):
        if self.handler.has_key(event):
            self.handler[event] = handler

    def dispatch(self, *args, **kwargs):
        # print 'dispatch'
        # print args
        if len(args) > 0:
            event = args[0]
            if self.handler.has_key(event):
                # print self.handler[event]
                return self.handler[event](*args, **kwargs)
        else:
            print 'error: no event'

#######################################################################################################################

class Test(Callbacks):
    EVT1 = 1
    EVT2 = 2

    def __init__(self):
        Callbacks.__init__(self)

        self.init([Test.EVT1, Test.EVT2])

    def cb1(self, event, str='', str2=''):
        print '11111'
        print str
        print str2

    def cb2(self, event, str):
        print '22222'
        print str

    def ttt(self):
        self.bind(Test.EVT1, self.cb1)
        # self.bind(Test.EVT2, self.cb2)

        self.dispatch(Test.EVT1, 'test 111')
        self.dispatch(Test.EVT2, 'test 222')

if __name__ == '__main__':
    test = Test()
    test.ttt()