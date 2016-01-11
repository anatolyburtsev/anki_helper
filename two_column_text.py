import re
import config
import dict_api
import helpers


class TwoColumnText:

    text = ""
    # TODO find right dash
    delimiter = " – "
    left_part_regexp = re.compile('[a-zA-Z\-]+')

    set_of_popular_words = helpers.get_popular_word(config.list_top_words)

    def __init__(self, text):
        self.text = text

    def split_string_to_words(self, line):
        if helpers.is_string_good(line, self.delimiter):
            words = self.left_part_regexp.findall(line)
            words = [x for x in words if x not in self.set_of_popular_words]
            return words
        else:
            return []

    def handle_text(self):
        result_text = ""
        for line in self.text.split('\n'):
            # здесь формируется вывод
            if not helpers.is_string_good(line, self.delimiter):
                continue
            words = self.split_string_to_words(line)
            eng_word, rus_word = line.split(self.delimiter)[0:2]
            result_line = helpers.handle_words_or_word(words).format(eng=eng_word, rus=rus_word, tab="\t")
            if result_line:
                result_text += result_line
                result_text += "\n"
        return result_text




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

t = TwoColumnText(txt)
print(t.handle_text())