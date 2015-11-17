__author__ = 'vin@misday.com'

import sqlite3

class SqliteHelp:
    def __init__(self, dbName = '', newVersion= 0):
        self.conn = sqlite3.connect(dbName, check_same_thread=False)
        self.cursor = self.conn.cursor()

        version = self.getVersion()
        if version == 0:
            self.onCreate()
        else:
            if version > newVersion:
                self.onDowngrade(version, newVersion)
            else:
                self.onUpgrade(version, newVersion)
        self.setVersion(newVersion)

    def __del__(self):
        self.cursor.close()
        self.conn.close()



    def getVersion(self):
        self.cursor.execute('PRAGMA user_version;')
        rows = self.cursor.fetchall()
        ver = rows[0][0]
        return ver

    def setVersion(self, ver = 0):
        self.cursor.execute('PRAGMA user_version = %d' % ver)
        self.conn.commit()

    def onCreate(self):
        pass
    def onUpgrade(self, version, newVersion):
        pass
    def onDowngrade(self, version, newVersion):
        pass