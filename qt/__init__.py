__author__ = 'vin@misday'

from PySide import QtCore, QtGui
from pyvin.core import Log

(IDX_TEXT, IDX_TIP, IDX_ID, IDX_ICON, IDX_HANDLER, IDX_ID2) = range(0, 6)

def _toString(qtString):
    return unicode(qtString.toUtf8(),'utf8', 'ignore').encode('gb2312')
