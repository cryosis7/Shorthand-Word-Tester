WRITE_MODE = True

# Prefixes MUST be at the beginning.
# A phrase is usually near the end but may have a extra characters like an 's' or 'ed' afterwards.
# A suffix MUST be on the end of the word
keys = {
    "prefixes": [],
    "phrases": [],
    "suffixes": [],
}


def set_phrases():
    phrases_file = open('key_phrases.txt', 'r')
    current_key = None

    for line in phrases_file:
        if line.startswith('#') or line == '\n':
            continue

        word = format_word(line)
        if word in keys:
            current_key = word
            continue

        if current_key in keys:
            keys[current_key].append(word)


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
    for prefix in keys["prefixes"]:
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

        for suffix in keys["suffixes"]:
            if formatted_word.endswith(suffix):
                write_word(word)
                found_word = True
                break
                
        if not found_word:
            for phrase in keys["phrases"]:
                if phrase in formatted_word:
                    write_word(word)
                    break


set_phrases()

out = open('dictionary_filtered.txt', 'w')
dictionary_file = open('dictionary_full.txt', 'r')

dictionary = dictionary_file.read().split('\n')

get_prefixes()
get_suffixes()

dictionary_file.close()
out.close()
