import sqlite3


class Database:
    PREFIX = 'prefix'
    PHRASE = 'phrase'
    SUFFIX = 'suffix'

    def __init__(self):
        self.connection = sqlite3.connect('data.db')
        self.cursor = self.connection.cursor()
        self.initiate()

    def initiate(self):
        self.cursor.executescript(
            "CREATE TABLE IF NOT EXISTS filters (name text NOT NULL, type_id INTEGER NOT NULL);"
            "CREATE TABLE IF NOT EXISTS type (name text NULL NULL UNIQUE);"
            "INSERT OR IGNORE INTO type (name) VALUES ('{}');"
            "INSERT OR IGNORE INTO type (name) VALUES ('{}');"
            "INSERT OR IGNORE INTO type (name) VALUES ('{}');".format(self.PREFIX, self.PHRASE, self.SUFFIX))
        self.connection.commit()

    def insert(self, name, filter):
        if filter == self.PREFIX or filter == self.PHRASE or filter == self.SUFFIX:
            self.cursor.execute(
                "INSERT OR IGNORE INTO filters (name, type_id) VALUES (?, (SELECT rowid FROM type WHERE name=?));",
                (name, filter))
            self.connection.commit()

    def display(self):
        self.cursor.execute("SELECT filters.name, type.name FROM filters, type WHERE filters.type_id = type.rowid;")
        rows = self.cursor.fetchall()
        for row in rows:
            print(row)


db = Database()
db.insert('under', db.PREFIX)
db.insert('logical', db.PHRASE)
db.display()
