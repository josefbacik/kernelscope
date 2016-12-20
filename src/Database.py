import MySQLdb
import MySQLdb.cursors
import sqlite3

# Shamefully copied from stackoverflow
def _dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

class Database:
    TYPE_MYSQL=1
    TYPE_SQLITE=2

    def __init__(self):
        self.db = None
        self.type = 0

    def connect_mysql(self, dbhost, dbuser, dbpassword, dbname):
        self.type = self.TYPE_MYSQL
        self.db = MySQLdb.connect(host=dbhost, user=dbuser, passwd=dbpassword,
                db=dbname, cursorclass=MySQLdb.cursors.DictCursor)

    def connect_sqlite(self, filename):
        self.type = self.TYPE_SQLITE
        self.db = sqlite3.connect(filename)
        self.db.row_factory = _dict_factory

    def cursor(self):
        return self.db.cursor()

    def arg_str(self):
        if self.type == self.TYPE_MYSQL:
            return '%s'
        elif self.type == self.TYPE_SQLITE:
            return '?'
        return ''

    def commit(self):
        self.db.commit()
