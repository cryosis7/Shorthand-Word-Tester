import sqlite3


class Database:
    PREFIX = 'prefix'
    PHRASE = 'phrase'
    SUFFIX = 'suffix'

    def __init__(self):
        self.connection = sqlite3.connect('data.db')
        self.connection.row_factory = lambda cursor, row: row[0]
        self.cursor = self.connection.cursor()

    def reset_database(self):
        self.cursor.executescript(
            "CREATE TABLE IF NOT EXISTS type (name text NOT NULL UNIQUE);"
            "CREATE TABLE IF NOT EXISTS filters(name text NOT NULL, type_id INTEGER NOT NULL,"
            "FOREIGN KEY(type_id) REFERENCES type(rowid));"
            "INSERT OR IGNORE INTO type (name) VALUES ('{}');"
            "INSERT OR IGNORE INTO type (name) VALUES ('{}');"
            "INSERT OR IGNORE INTO type (name) VALUES ('{}');".format(self.PREFIX, self.PHRASE, self.SUFFIX))
        self.connection.commit()

    # Adds a single entry into the filters table.
    def add_filter(self, filter_name, filter_type):
        if filter_type == self.PREFIX or filter_type == self.PHRASE or filter_type == self.SUFFIX:
            sql = "SELECT name FROM filters WHERE name=? AND type_id=(SELECT rowid FROM type WHERE name=?);"
            if not self.cursor.execute(sql, (filter_name, filter_type)).fetchone():
                self.cursor.execute(
                    "INSERT INTO filters (name, type_id) VALUES (?, (SELECT rowid FROM type WHERE name=?));",
                    (filter_name, filter_type))
                self.connection.commit()

    # Adds a list of entries into the filters table.
    def add_filters(self, filters_list, filter_type):
        if filter_type == self.PREFIX or filter_type == self.PHRASE or filter_type == self.SUFFIX:
            for filter_name in filters_list:
                sql = "SELECT name FROM filters WHERE name=? AND type_id=(SELECT rowid FROM type WHERE name=?);"
                if not self.cursor.execute(sql, (filter_name, filter_type)).fetchone():
                    self.cursor.execute(
                        "INSERT INTO filters (name, type_id) VALUES (?, (SELECT rowid FROM type WHERE name=?));",
                        (filter_name, filter_type))
            self.connection.commit()

    def clear_database(self):
        self.cursor.executescript("DROP TABLE IF EXISTS filters;"
                                  "DROP TABLE IF EXISTS type;")
        self.reset_database()

    # Returns all filters in the database as 3 lists in a dictionary, separated by filter type.
    def get_all_filters(self):
        filters = {
            self.PREFIX: [],
            self.PHRASE: [],
            self.SUFFIX: [],
        }
        sql = "SELECT name FROM filters WHERE type_id=(SELECT rowid FROM type WHERE name=?) ORDER BY name"
        self.cursor.execute(sql, (self.PREFIX,))
        filters[self.PREFIX] = self.cursor.fetchall()
        self.cursor.execute(sql, (self.PHRASE,))
        filters[self.PHRASE] = self.cursor.fetchall()
        self.cursor.execute(sql, (self.SUFFIX,))
        filters[self.SUFFIX] = self.cursor.fetchall()
        return filters

    # Returns a list of the filters that match the filter type
    def get_filters(self, filter_type):
        filter_list = []
        if filter_type == self.PREFIX or filter_type == self.PHRASE or filter_type == self.SUFFIX:
            sql = "SELECT name FROM filters WHERE type_id=(SELECT rowid FROM type WHERE name=?) ORDER BY name"
            self.cursor.execute(sql, (filter_type,))
            filter_list = self.cursor.fetchall()
        return filter_list

    # Deletes a single entry from the filter
    def delete_filter(self, filter_name, filter_type):
        if filter_type == self.PREFIX or filter_type == self.PHRASE or filter_type == self.SUFFIX:
            sql = "DELETE FROM filters WHERE name LIKE ? AND type_id=(SELECT rowid FROM type WHERE name LIKE ?);"
            self.cursor.execute(sql, (filter_name, filter_type))
            self.connection.commit()

    # Will delete all filters out of the dictionary.
    # If a filter_type is given, will delete all of that type.
    def delete_all_filters(self, filter_type=None):
        if filter_type is None:
            self.cursor.execute("DELETE FROM filters")
            self.connection.commit()
        elif filter_type == self.PREFIX or filter_type == self.PHRASE or filter_type == self.SUFFIX:
            sql = "DELETE FROM filters WHERE type_id=(SELECT rowid FROM type WHERE name LIKE ?);"
            self.cursor.execute(sql, (filter_type,))
            self.connection.commit()

    # Will return an unordered list of the filtered dictionary set
    def get_dictionary(self):
        self.cursor.execute("SELECT * FROM dictionary_full AS d JOIN filters AS f ON ( " +
                            "CASE f.type_id " +
                            "WHEN 1 THEN d.word LIKE f.name || '%' " +
                            "WHEN 2 THEN d.word LIKE '%' || f.name || '%' " +
                            "WHEN 3 THEN d.word LIKE '%' || f.name " +
                            "END) " +
                            "GROUP BY d.word;")
        return self.cursor.fetchall()

    def close(self):
        self.connection.close()

#
# db = Database()
# db.close()
