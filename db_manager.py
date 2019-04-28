import sqlite3


class Database:
    PREFIX = 'prefix'
    PHRASE = 'phrase'
    SUFFIX = 'suffix'

    def __init__(self):
        self.connection = sqlite3.connect('data.db')
        self.connection.row_factory = lambda cursor, row: row[0]
        self.cursor = self.connection.cursor()
        self.initiate()

    def initiate(self):
        self.cursor.executescript(
            "CREATE TABLE IF NOT EXISTS type (name text NULL NULL UNIQUE);"
            "CREATE TABLE IF NOT EXISTS filters(name text NOT NULL, type_id INTEGER NOT NULL,"
            "FOREIGN KEY(type_id) REFERENCES type(rowid));"
            "INSERT OR IGNORE INTO type (name) VALUES ('{}');"
            "INSERT OR IGNORE INTO type (name) VALUES ('{}');"
            "INSERT OR IGNORE INTO type (name) VALUES ('{}');".format(self.PREFIX, self.PHRASE, self.SUFFIX))
        self.connection.commit()

    def add_filter(self, filter_name, filter_type):
        if filter_type == self.PREFIX or filter_type == self.PHRASE or filter_type == self.SUFFIX:
            sql = "SELECT name FROM filters WHERE name=? AND type_id=(SELECT rowid FROM type WHERE name=?);"
            if not self.cursor.execute(sql, (filter_name, filter_type)).fetchone():
                self.cursor.execute(
                    "INSERT INTO filters (name, type_id) VALUES (?, (SELECT rowid FROM type WHERE name=?));",
                    (filter_name, filter_type))
                self.connection.commit()

    def add_filters(self, filters_list, filter_type):
        if filter_type == self.PREFIX or filter_type == self.PHRASE or filter_type == self.SUFFIX:
            for filter in filters_list:
                sql = "SELECT name FROM filters WHERE name=? AND type_id=(SELECT rowid FROM type WHERE name=?);"
                if not self.cursor.execute(sql, (filter, filter_type)).fetchone():
                    self.cursor.execute(
                        "INSERT INTO filters (name, type_id) VALUES (?, (SELECT rowid FROM type WHERE name=?));",
                        (filter, filter_type))
            self.connection.commit()

    def display(self):
        self.cursor.execute("SELECT filters.name, type.name FROM filters, type WHERE filters.type_id = type.rowid;")
        rows = self.cursor.fetchall()
        for row in rows:
            print(row)

    def clear_database(self):
        self.cursor.executescript("DROP TABLE IF EXISTS filters;"
                                  "DROP TABLE IF EXISTS type;")
        self.initiate()

    # Returns all filters in the database as a dictionary, separated by filter type.
    def get_filters(self):
        filters = {
            self.PREFIX: [],
            self.PHRASE: [],
            self.SUFFIX: [],
        }
        sql = "SELECT name FROM filters WHERE type_id=(SELECT rowid FROM type WHERE name=?)"
        self.cursor.execute(sql, (self.PREFIX,))
        filters[self.PREFIX] = self.cursor.fetchall()
        self.cursor.execute(sql, (self.PHRASE,))
        filters[self.PHRASE] = self.cursor.fetchall()
        self.cursor.execute(sql, (self.SUFFIX,))
        filters[self.SUFFIX] = self.cursor.fetchall()
        return filters

    def close(self):
        self.connection.close()


# db = Database()
# db.clear_database()
# db.get_filters()

# db.insert('under', db.PREFIX)
# db.insert('logical', db.PHRASE)
# db.insert('auto', db.PREFIX)
# li = db.get_filters()
# for l in li:
#     print(l + ":")
#     for x in li[l]:
#         print(x)
#     print("\n")
# db.display()
# db.close()
