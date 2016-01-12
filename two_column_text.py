import re
import config
import dict_api
import helpers
import vk_api
import os.path
import logging

logging.basicConfig(format=u'%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s',
                    level=logging.ERROR)


class TwoColumnText:
    text = ""
    url = ""
    handled_text = ""
    # TODO find right dash
    delimiter = " – "
    left_part_regexp = re.compile('[a-zA-Z\-]+')

    set_of_popular_words = helpers.get_popular_word(config.list_top_words)

    def __init__(self, text, url):
        self.text = text
        self.url = url

    def split_string_to_words(self, line):
        if helpers.is_string_good(line, self.delimiter):
            words = self.left_part_regexp.findall(line)
            words = [x for x in words if x not in self.set_of_popular_words]
            return words
        else:
            return []

    def handle_text(self, line_delimiter="\n"):
        result_text = ""
        for line in self.text.split(line_delimiter):
            # здесь формируется вывод
            if not helpers.is_string_good(line, self.delimiter):
                continue
            words = self.split_string_to_words(line)
            eng_word, rus_word = line.split(self.delimiter)[0:2]
            result_line = helpers.handle_words_or_word(words).format(eng=eng_word, rus=rus_word, tab="\t")
            if result_line:
                result_text = result_text + result_line + "\n"
        self.handled_text = result_text
        return result_text

    def save_handled_text(self, dir_to_save=config.result_share):
        if not self.handled_text:
            self.handle_text()
        filename = self.url.split('/')[-1] + ".txt"
        path_to_file = os.path.join(dir_to_save, filename)
        helpers.save_text_to_file(self.handled_text, path_to_file)
        return path_to_file


if __name__ == "__main__":

    txt = """trachea, windpipe – трахея.
bronchial tube, bronchus – бронх.
bronchi – бронхи.
lungs – легкие.

heart – сердце.
ventricle – желудочек (сердца, мозга).
auricle – предсердие.
cardiac valve – сердечный клапан.
vein – вена.
artery – артерия.
aorta – аорта.
coronary artery – коронарная артерия.
carotid – сонная артерия.

pharynx – глотка."""

    # t = TwoColumnText(txt)
    # print(t.handle_text())

    url = "https://vk.com/wall-87512171_139"
    txt = vk_api.url_to_post_text_converter(url)
    t = TwoColumnText(txt)
    result = t.handle_text()
    print(result)