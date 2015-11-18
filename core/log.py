__author__ = 'vin@misday.com'

from pyvin.core import Callbacks

class Log(Callbacks):
    @staticmethod
    def d(str):
        print 'D: %s' % (str, )

    @staticmethod
    def v(str):
        print 'V: %s' % (str, )

    @staticmethod
    def i(str):
        print 'I: %s' % (str, )

    @staticmethod
    def w(str):
        print 'W: %s' % (str, )

    @staticmethod
    def e(str):
        print 'E: %s' % (str, )