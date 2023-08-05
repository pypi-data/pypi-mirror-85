# Part of odoo-build.
# See LICENSE file for full copyright and licensing details.

import psycopg2


class Database():
    def __init__(self, conf):
        self.settings = conf['database']
        self.conn = None

    def connect(self, dbname='postgres'):
        self.disconnect()
        self.conn = psycopg2.connect(dbname=dbname, **self.settings)
        return self

    def disconnect(self):
        if self.conn:
            self.conn.close()

    def cr(self):
        return self.conn.cursor()
