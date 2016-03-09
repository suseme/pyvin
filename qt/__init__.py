__author__ = 'vin@misday'

from PySide import QtCore, QtGui
from pyvin.core import Log

def _toString(qtString):
    return unicode(qtString.toUtf8(),'utf8', 'ignore').encode('gb2312')
