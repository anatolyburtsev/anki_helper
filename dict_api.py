import config
import requests
import json
import logging


def get_available_languages(finish_with="en", key=config.dict_key):
    req_langs = "https://dictionary.yandex.net/api/v1/dicservice.json/getLangs?key={}".format(key)
    available_languages = requests.get(req_langs)
    if available_languages.status_code != 200:
        logging.error("Error getting available language list")

    available_languages = [x for x in json.loads(available_languages.text)
                           if x.endswith("-"+finish_with) and x != "en-en" ]
    return available_languages


def lookup_ts_pos_force(text, key=config.dict_key):
    ui = "en"
    available_languages = get_available_languages("en")
    additional_date = lookup_ts_pos(text)
    if additional_date["ts"] or additional_date["pos"]:
        return additional_date
    for lang in available_languages:
        additional_date = lookup_ts_pos(text, lang)
        # print(additional_date)
        if additional_date["ts"] or additional_date["pos"]:
            break
    return additional_date


def lookup_ts_pos(word, lang="en-en", key=config.dict_key, ui="en"):
    # https://dictionary.yandex.net/api/v1/dicservice.json/lookup?key=dict.1.1.20160106T144241Z.c1a1cf55a776643c.803d1e827d414dbf3d957bd3f683778a6ed29fc1&text=hello&lang=en-en&ui=en
    assert type(word) == str
    assert len(word.split(' ')) == 1
    attempts = 5
    req = 'https://dictionary.yandex.net/api/v1/dicservice.json/lookup?key={}&text={}&lang={}&ui={}'.format(
        key, word, lang, ui
    )
    empty_response = '{"head":{},"def":[]}'

    for i in range(attempts):
        try:
            response = requests.get(req)
        except:
            if i + 1 != attempts:
                logging.info("Couldn't get info for word:" + word + ". Try again.")
            else:
                logging.error("Couldn't get info for word:" + word)
                raise
        else:
            break
    if response.status_code != 200:
        logging.error("problem with request:{}".format(req))
    # print("req=" + req)
    # print("response=" + response.text)
    if response.text == empty_response:
        return {"ts": "", "pos": ""}
    try:
        response = json.loads(response.text)
    except:
        logging.error('problem with jsoning word:' + word)
        return {"ts": "", "pos": "", "word": word}

    response = response["def"][0]
    if "ts" in response.keys():
        ts = response["ts"]
    else:
        ts = ""
    # Part Of Speech
    if "pos" in response.keys():
        pos = response["pos"]
    else:
        pos = ""
    return {"ts": ts, "pos": pos}

if __name__ == "__main__":
    # print(dir(dict))
    print(lookup_ts_pos_force("bronchi"))

    pass
