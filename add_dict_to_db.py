from db_manager import Database

db = Database()
dictionary_file = open('dictionary_filtered.txt', 'r')
dictionary = dictionary_file.read().split('\n')

db.cursor.execute("CREATE TABLE IF NOT EXISTS dictionary_filtered (word text NOT NULL UNIQUE);")
for word in dictionary:
    clean_word = ''.join([i for i in word.lower() if i.isalpha() or i == '-'])
    if clean_word:
        db.cursor.execute("INSERT OR IGNORE INTO dictionary_filtered (word) VALUES ('{}')".format(clean_word))

db.connection.commit()

dictionary_file.close()
db.close()
