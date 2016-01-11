#!/bin/env python3
import sys


def convert_string(st):
    """
    >>> convert_string("hooked;попался на крючек;http://d144fqpiyasmrr.cloudfront.net/uploads/picture/1747634.png;hˈʊkt;Suburgatory: This ABC sitcom snuck up on us last season, and we’re totally <b>hooked</b> now;http://d2x1jgnvxlnz25.cloudfront.net/v2/1/19967-631152008.mp3")
    ('hooked', 'попался на крючек', 'hˈʊkt', 'Suburgatory: This ABC sitcom snuck up on us last season, and we’re totally <b>hooked</b> now')

    :param str:
    :return tuple of str:
    """
    if not st:
        return
    st = st.split(";")
    assert len(st) > 4
    return (st[0].strip(), st[1].strip(), st[3].strip(), st[4].strip())


def format_string(tpl):
    """
    >>> format_string(('to immerse', 'погружать', 'ˌɪˈmɝs', 'Yet even while <b>immersed</b> in an optimism bubble with these young people, I could see the strains that came with Google’s abrupt growth from a feisty start-up to a market-dominating giant with more than 20,000 employees.'))
    'to immerse<br/><span style="color: #666;">/ˌɪˈmɝs/</span><br/><br/>Yet even while <b>immersed</b> in an optimism bubble with these young people, I could see the strains that came with Google’s abrupt growth from a feisty start-up to a market-dominating giant with more than 20,000 employees.  погружать'

    :param tpl:
    :return str:
    """
    assert len(tpl) == 4
    eng_word, rus_word, trans, example = tpl
    result_string = "{}<br/><span style=\"color: #666;\">/{}/</span><br/><br/>{}\t{}\n".format(eng_word, trans, example, rus_word)
    return result_string


def extract_from_full_text(input_file, output_file):
    """
    extract just english word from list of known words from wordsfromtext
    :param filename:
    :return:
    """
    fw = open(output_file, 'w')
    with open(input_file, 'r') as f:
        st = f.readline()
        while st:
            word = st.split('\t')[0] + "\n"
            if word.startswith("to ") or word.startswith("an ") or word.startswith("at ") or word.startswith("in "):
                word = word[3:]
            if word.startswith("a "):
                word = word[2:]
            if word.strip().endswith(" of"):
                word = word[:-3]
            fw.writelines(word)
            st = f.readline()
    fw.close()


def additional_convert():
    # доконвертирование после вытаскивание словаря из Leo с помощью плагина Anki-Leo для Chrome
    try:
        # file_to_convert = int(sys.argv[1])
        file_to_convert = "leo.csv"
        file_to_output = "output.txt"
    except (TypeError, ValueError, IndexError):
        sys.exit("Usage: additional_convert.py file.csv (output.txt)")

    fw = open(file_to_output, 'w')

    with open(file_to_convert, 'r') as f:
        st = f.readline()
        while st:
            tpl = convert_string(st)
            fw.writelines(format_string(tpl))
            st = f.readline()
    fw.close()

if __name__ == "__main__":
    pass
    # extract_from_full_text("/Users/onotole/Downloads/onotole_fulltext.txt", "/Users/onotole/Downloads/list_popular_word.txt")