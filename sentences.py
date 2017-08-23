import re


def parse_sent(text):
    sentences = []
    if text:
        text = clean_text(text)
        char_pos = 0
        sent_pos = 0
        sentence = ""
        in_quotes = False
        # loop characters in text
        for a in text:
            # are we in quotes?
            if a == '"':
                in_quotes = not in_quotes
            # end of sentence char?
            if a in EOS_CHARS:
                if a == '.':
                    sent_pos += 1
                elif a == '!':
                    sent_pos += 1
                elif a == '?':
                    sent_pos += 1
            sentence += a
            char_pos += 1
    return sentences