import dict_api
import re
import logging

ENGLISH_LETTERS = set(['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','v','u','w','x',
                      'y','z'])
RUSSIAN_LETTERS = set(['а','б','в','г','д','е','ё','ж','з','и','й','к','л','м','н','о','п','р','с','т','у','ф','х','ц',
                      'ч','ш','щ','ъ','ы','ь','э','ю','я'])

def get_popular_word(filename):
    # TODO check file for exist
    f = open(filename, 'r')
    s = f.readline()
    result = set(s[:-1])
    while s:
        s = f.readline()
        if s:
            result.add(s[:-1])
    return result


def save_text_to_file(text, filename):
    with open(filename, 'w') as f:
        f.write(text)


def is_string_good(line, delimiter):
        if not line:
            return False
        if len(line.split(delimiter)) != 2:
            return False
        return True


def make_beauty_1_word(words_dict):
    # input: {"ts": ts, "pos": pos, "word": word }
    # output: <span style="color: #aaa;">(adv.)</span> actually<br/><span style="color: #666;">/ˈæˌktʃuəli, ˈæktʃli, ˈækʃəli/</span>	на самом деле
    result = '<span style="color: #aaa;">{pos}</span> {word}<br/><span style="color: #666;">{ts}</span>{tab}{rus}'
    pos = ts = ""
    if words_dict["pos"]:
        pos = "(" + words_dict["pos"] + ")"
    if words_dict["ts"].strip():
        ts = "/ " + words_dict["ts"] + " /"
    return result.format(pos=pos, word="{eng}", ts=ts, rus="{rus}", tab="{tab}")


def make_beauty_some_words(words_dict, pos):
    result = '<span style="color: #aaa;">{pos}</span> {word}<br/><span style="color: #666;">{ts}</span>{tab}{rus}'
    ts = "/"
    if pos:
        pos = "(" + pos + ")"
    for word in words_dict:
        if word["ts"].strip() != "":
            ts = ts + " " + word["ts"] + " "
    ts += "/"
    if ts == "//":
        ts = ""
    return result.format(pos=pos, word="{eng}", ts=ts, rus="{rus}", tab="{tab}")


def handle_words(words):
    assert type(words) == list
    assert len(words) > 1
    words_external = []
    for word in words:
        if len(word) > 2:
            words_external.append(dict_api.lookup_ts_pos_force(word))

    pos = ""
    for word in words_external:
        if word["pos"]:
            pos = word["pos"]
            break
    for word in words_external:
        if word["pos"] and word["pos"] != pos:
            pos = ""
            break

    return make_beauty_some_words(words_external, pos)


def handle_words_or_word(words):
        assert type(words) == list
        if len(words) == 0:
            return ""
        if len(words) == 1:
            ts_pos = dict_api.lookup_ts_pos_force(words[0])
            return make_beauty_1_word(ts_pos)
        else:
            return handle_words(words)


def find_delimiter(text, dash_types=False):
    """
    >>> find_delimiter("resume - резюме")
    ' - '
    >>> find_delimiter("occupation — занятие")
    ' — '
    >>> find_delimiter('unemployed / jobless / out-of-work / man out of occupation - безработный')
    ' - '
    >>> find_delimiter("lose (lost, lost) one's job - потерять работу")
    ' - '
    >>> find_delimiter('lump-sum allowance - единовременное пособие')
    ' - '
    >>> find_delimiter('lump-sum allowance — единовременное пособие')
    ' — '
    >>> find_delimiter("43. What's the idea of - В чём смысл, что за глупость -")
    ' - '
    >>> find_delimiter('Мне нужно лекарство от простуды. — I need a cold medicine.')
    ' — '

    :param text:
    :return dash:
    """

    # in PyCharm they looks similar, but they are differ
    if not dash_types:
        dash_types = [' — ', ' - ', ' - ']

    # current dash is right if it's relevant for more then koeff*100% strings.
    koeff = 0.5

    for dash in dash_types:
        all_line = 0
        suitable_for_this_delimiter = 0
        for line in text.split("\n"):
            if line.strip() != "":
                all_line += 1
            if len(line.split(dash)) == 2:
                l_part, r_part = line.split(dash)
                if is_english(l_part) and is_russian(r_part) or is_russian(l_part) and is_english(r_part):
                    suitable_for_this_delimiter += 1
        if float(suitable_for_this_delimiter)/all_line > koeff:
            return dash

    # logging.error("delimiter not found. text:" + text)
    return False


def find_delimiter_euristic(text):
    """
    :param text:
    :return delimiter:
    """

    handled_text = []
    possible_delimiter = []
    for line in text.split("\n"):
        if line.strip() != "" and re.search("[a-zA-Z]+", line) and re.search("[а-яА-Я]+", line):
            handled_text.append(line)

    for line in handled_text:
        possible_delimiter.append(find_delimiter_euristic_line(line))

    delimiters_dict = {}
    for d in possible_delimiter:
        if d not in delimiters_dict.keys():
            delimiters_dict[d] = 1
        else:
            delimiters_dict[d] += 1

    delimiter_amount_max = 0
    delimiter_most_popular = ""
    for delimiter, delimiter_amount in delimiters_dict.items():
        if delimiter_amount > delimiter_amount_max:
            delimiter_amount = delimiter_amount_max
            delimiter_most_popular = delimiter

    return delimiter_most_popular


def find_delimiter_euristic_line(line):
    """
    >>> find_delimiter_euristic_line("startle at smth– вздрогнуть от чего-то")
    '–'
    >>> find_delimiter_euristic_line(" pew/PEW-wow @ пышь/ПЫШЬ")
    '@'
    >>> find_delimiter_euristic_line("  пышь/ПЫШЬ @  pew/PEW-wow ")
    '@'

    :param line:
    :return:
    """
    finish_1st_part = 0
    start_2nd_part = 0
    line = line.strip().lower()
    # Eng -> Rus
    if line[0] in ENGLISH_LETTERS:
        first_languages_letters = ENGLISH_LETTERS
        second_langueage_letters = RUSSIAN_LETTERS
    else:
        first_languages_letters = RUSSIAN_LETTERS
        second_langueage_letters = ENGLISH_LETTERS

    for letter_no in range(len(line)):
        if line[letter_no] in first_languages_letters:
            finish_1st_part = letter_no
        if line[letter_no] in second_langueage_letters and not start_2nd_part:
            start_2nd_part = letter_no

    if start_2nd_part > finish_1st_part:
        print("problem with euristic detection delimiter in line: {}".format(line))
    delimiter = line[finish_1st_part+1:start_2nd_part].strip()
    return delimiter



def is_english(text):
    """
    >>> is_english('abc')
    True
    >>> is_english('unemployed / jobless / out-of-work / man out of occupation - ')
    True
    >>> is_english('43. Whats the idea of - В чём смысл, что за глупость -')
    False

    :param text:
    :return boolean:
    """
    if re.findall('[а-яА-Я]+', text):
        return False
    else:
        return True


def is_russian(text):
    """
    >>> is_russian("абв")
    True
    >>> is_russian('43. Whats the idea of - В чём смысл, что за глупость -')
    False
    >>> is_russian("Хотите за 3 минуты узнать свой словарный запас английских слов? ")
    True

    :param text:
    :return boolean:
    """
    if re.findall('[a-zA-Z]+', text):
        return False
    else:
        return True


if __name__ == "__main__":
    # dt = {"ts": "ˈæˌktʃuəli, ˈæktʃli, ˈækʃəli", "pos": "adv.", "word": "actually" }
    # print(make_beauty_1_word(dt))
    # words = [{"ts": "ˈkɒrən(ə)rɪ", "pos": "noun.", "word": "coronary" },
    #          {"ts": "ˈɑːtərɪ", "pos": "noun", "word": "artery"},
    #          {"ts": "veɪn", "pos": "", "word": "vein"}]
    # # print(make_beauty_some_words(words, "noun."))
    # # print(handle_words(["bronchi", "artery", "vein"]))
    # print(is_english("abя"))

    # test euristic_delimiter_finder
    text = """СТРАХ

feel sick at smth – слабеть при виде чего-то

pallid at smth – побледневший от чего-то

startle at smth– вздрогнуть от чего-то

aghast at smth – пораженный ужасом при виде

appalled at / with smth – устрашенный чем-то

dismayed at / with smth – приведенный в ужас чем-то

frightened at smth – испуганный чем-то

horrified at smth – в ужасе от чего-то
"""

    print( find_delimiter_euristic(text))
    print (find_delimiter_euristic_line("startle at smth– вздрогнуть от чего-то"))
