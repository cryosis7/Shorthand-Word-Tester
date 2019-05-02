from db_manager import Database

db = Database()
phrases_file = open('key_phrases.txt', 'r')
phrases = phrases_file.read().split('\n')

db.cursor.execute("CREATE TABLE IF NOT EXISTS filters"
                  "(name text NOT NULL, type_id INTEGER NOT NULL, FOREIGN KEY(type_id) REFERENCES type(rowid))")

type_id = 0
for word in phrases:
    if word.startswith('#') or word.startswith(' '):
        continue
    elif word == "PREFIXES" or word == "PHRASES" or word == "SUFFIXES":
        type_id += 1
        continue

    clean_word = ''.join([i for i in word.lower() if i.isalpha() or i == '-'])
    if clean_word:
        db.cursor.execute("INSERT OR IGNORE INTO filters (name, type_id) VALUES (?, ?)", (clean_word, type_id))

db.connection.commit()

phrases_file.close()
db.close()
