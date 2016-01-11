import dict_api


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
    return result.format(pos=pos, ts=ts, word="{eng}", rus="{rus}", tab="{tab}") #words_dict["word"])


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


if __name__ == "__main__":
    dt = {"ts": "ˈæˌktʃuəli, ˈæktʃli, ˈækʃəli", "pos": "adv.", "word": "actually" }
    print(make_beauty_1_word(dt))
    words = [{"ts": "ˈkɒrən(ə)rɪ", "pos": "noun.", "word": "coronary" },
             {"ts": "ˈɑːtərɪ", "pos": "noun", "word": "artery"},
             {"ts": "veɪn", "pos": "", "word": "vein"}]
    # print(make_beauty_some_words(words, "noun."))
    print(handle_words(["bronchi", "artery", "vein"]))

