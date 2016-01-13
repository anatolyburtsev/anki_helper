import dict_api
import re
import logging


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
    if words_dict["ts"]:
        ts = "/ " + words_dict["ts"] + " /"
    return result.format(pos=pos, word="{eng}", ts=ts, rus="{rus}", tab="{tab}")


def make_beauty_some_words(words_dict, pos):
    result = '<span style="color: #aaa;">{pos}</span> {word}<br/><span style="color: #666;">{ts}</span>{tab}{rus}'
    ts = "/"
    if pos:
        pos = "(" + pos + ")"
    for word in words_dict:
        if word["ts"]:
            ts = ts + " " + word["ts"] + " "
    ts += "/"
    return result.format(pos=pos, word="{eng}", ts=ts, rus="{rus}", tab="{tab}")


def handle_words(words):
    assert type(words) == list
    assert len(words) > 1
    words_external = []
    for word in words:
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


def find_delimiter(text):
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
    dash_types = [' — ', ' - ', ' - ']

    # current dash is right if it's relevant for more then koeff*100% strings.
    koeff = 0.5

    for dash in dash_types:
        all_line = 0
        suitable_for_this_delimiter = 0
        for line in text.split("\n"):
            if line:
                all_line += 1
            if len(line.split(dash)) == 2:
                l_part, r_part = line.split(dash)
                if is_english(l_part) and is_russian(r_part) or is_russian(l_part) and is_english(r_part):
                    suitable_for_this_delimiter += 1
        if float(suitable_for_this_delimiter)/all_line > koeff:
            return dash

    logging.error("delimiter not found. text:" + text)
    return dash_types[0]






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
    dt = {"ts": "ˈæˌktʃuəli, ˈæktʃli, ˈækʃəli", "pos": "adv.", "word": "actually" }
    print(make_beauty_1_word(dt))
    words = [{"ts": "ˈkɒrən(ə)rɪ", "pos": "noun.", "word": "coronary" },
             {"ts": "ˈɑːtərɪ", "pos": "noun", "word": "artery"},
             {"ts": "veɪn", "pos": "", "word": "vein"}]
    # print(make_beauty_some_words(words, "noun."))
    # print(handle_words(["bronchi", "artery", "vein"]))
    print(is_english("abя"))
