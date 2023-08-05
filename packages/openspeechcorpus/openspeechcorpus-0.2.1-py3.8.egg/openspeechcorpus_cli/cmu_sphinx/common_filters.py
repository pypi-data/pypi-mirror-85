
def clean_accents(word):
    output = []
    for letter in word:
        if letter == u"á":
            modified_letter = "a"
        elif letter == u"é":
            modified_letter = "e"
        elif letter == u"í":
            modified_letter = "i"
        elif letter == u"ó":
            modified_letter = "o"
        elif letter == u"ú":
            modified_letter = "u"
        elif letter == u"ñ":
            modified_letter = "N"
        else:
            modified_letter = letter
        output.append(modified_letter)
    return ''.join(output)


def filter_special_characters(word):
    output = []
    for letter in word:
        if letter == u"-":
            modified_letter = ""
        elif letter == u"\n":
            modified_letter = ""
        elif letter == u"\.":
            modified_letter = ""
        elif letter == u"?":
            modified_letter = ""
        else:
            modified_letter = letter
        output.append(modified_letter)
    return ''.join(output)


def allow_characters(word):
    alphabet = "abcdefghijklmnNopqrstuvwxyz "
    output = []
    for letter in word:
        if letter in alphabet:
            output.append(letter)
    return ''.join(output)


def extract_phones_from_word(word):
    return ' '.join(apply_filters(word))


def apply_filters(word):
    return allow_characters(filter_special_characters(clean_accents(word)))


def remove_jump_characters(word):
    return word.replace("\n", "").replace("\r", "")
