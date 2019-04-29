import db_manager
WRITE_MODE = True

filters = {}


def set_phrases():
    global filters
    db = db_manager.Database()
    filters = db.get_filters()
    db.close()


def format_word(word):
    word = word.lower()
    word = ''.join([i for i in word if i.isalpha() or i == '-'])
    return word


def write_word(word, index=None):
    if WRITE_MODE:
        out.write(format_word(word) + '\n')
    else:
        print(format_word(word))
    if index is None:
        dictionary.pop(dictionary.index(word))
    else:
        dictionary.pop(index)


def get_prefixes():
    for prefix in filters[db_manager.Database.PREFIX]:
        try:
            index = dictionary.index(prefix)
            while dictionary[index].startswith(prefix):
                write_word(dictionary[index], index)

        except ValueError:
            pass


def get_suffixes():
    for word in dictionary:
        formatted_word = format_word(word)
        found_word = False

        for suffix in filters[db_manager.Database.SUFFIX]:
            if formatted_word.endswith(suffix):
                write_word(word)
                found_word = True
                break
                
        if not found_word:
            for phrase in filters[db_manager.Database.PHRASE]:
                if phrase in formatted_word:
                    write_word(word)
                    break


set_phrases()

out = open('dictionary_filtered_sql.txt', 'w')
dictionary_file = open('dictionary_full.txt', 'r')

dictionary = dictionary_file.read().split('\n')

get_prefixes()
get_suffixes()

dictionary_file.close()
out.close()
