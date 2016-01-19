__author__ = 'vin@misday.com'

from pyvin.core import Callbacks

class Log(Callbacks):
    @staticmethod
    def d(tag, msg):
        print 'D: [%s] %s' % (tag, msg)

    @staticmethod
    def v(tag, msg):
        print 'V: [%s] %s' % (tag, msg)

    @staticmethod
    def i(tag, msg):
        print 'I: [%s] %s' % (tag, msg)

    @staticmethod
    def w(tag, msg):
        print 'W: [%s] %s' % (tag, msg)

    @staticmethod
    def e(tag, msg):
        print 'E: [%s] %s' % (tag, msg)