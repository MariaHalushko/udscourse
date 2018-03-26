# -*- coding: utf-8 -*-
import re

from nltk.tokenize import word_tokenize

TOKEN_LINK = "LINK"
PUNCTUATION = {'.', '?', '!'}
TOKENS = {TOKEN_LINK}

repl = {
    "yay!": " good ",
    "yay": " good ",
    "yaay": " good ",
    "yaaay": " good ",
    "yaaaay": " good ",
    "yaaaaay": " good ",
    ":/": " bad ",
    ":&gt;": " sad ",
    ":')": " sad ",
    ":-(": " frown ",
    ":(": " frown ",
    ":s": " frown ",
    ":-s": " frown ",
    "&lt;3": " heart ",
    ":d": " smile ",
    ":p": " smile ",
    ":dd": " smile ",
    "8)": " smile ",
    ":-)": " smile ",
    ":)": " smile ",
    ";)": " smile ",
    "(-:": " smile ",
    "(:": " smile ",
    ":/": " worry ",
    ":&gt;": " angry ",
    ":')": " sad ",
    ":-(": " sad ",
    ":(": " sad ",
    ":s": " sad ",
    ":-s": " sad ",
    r"\br\b": "are",
    r"\bu\b": "you",
    r"\bhaha\b": "ha",
    r"\bhahaha\b": "ha",
    r"\bdon't\b": "do not",
    r"\bdoesn't\b": "does not",
    r"\bdidn't\b": "did not",
    r"\bhasn't\b": "has not",
    r"\bhaven't\b": "have not",
    r"\bhadn't\b": "had not",
    r"\bwon't\b": "will not",
    r"\bwouldn't\b": "would not",
    r"\bcan't\b": "can not",
    r"\bcannot\b": "can not",
    r"\bi'm\b": "i am",
    "m": "am",
    "r": "are",
    "u": "you",
    "haha": "ha",
    "hahaha": "ha",
    "don't": "do not",
    "doesn't": "does not",
    "didn't": "did not",
    "hasn't": "has not",
    "haven't": "have not",
    "hadn't": "had not",
    "won't": "will not",
    "wouldn't": "would not",
    "can't": "can not",
    "cannot": "can not",
    "i'm": "i am",
    "m": "am",
    "i'll": "i will",
    "its": "it is",
    "it's": "it is",
    "'s": " is",
    "that's": "that is",
    "weren't": "were not",
}


def tokenize(text, link_token=TOKEN_LINK):
    text = text.lower()
    text = replace_links(text, link_token)
    text = _add_missing_spaces(text)
    text = _remove_unnecessary_symbols(text)

    tokens = [t for t in word_tokenize(text) if t.isalpha() or t == link_token or t in PUNCTUATION]
    tokens = _replace_key_words(tokens)
    return tokens


def get_count_significant_words(list_of_words):
    """
    :param list_of_words:
    :return: number of significant word. Word is significant if that is not a punctuation and not a special token.
    """
    return len([w for w in list_of_words if (w not in (PUNCTUATION | TOKENS))])


def replace_links(text, token=TOKEN_LINK):
    # some links begin with http or https: https?://\S+
    # link can begins with www: www\.\S+
    # links to google documents: \\bgoo\.gl/\w+/?
    # else:
    #   hostname usually have some domain names separated by dot: (\w+\.){2,4}
    #   last domain name can have min 2 and max 6 letters: ([a-z]{2,6})
    #   if path exists - it can be separated by / and must begins with /: (/\S+)*
    #   link can have / in the end: /?
    # to match some links with 1 dot we check if exists path after hostname:
    #   hostname: \w+\.([a-z]{2,6})
    #   path: /(\S+/)*(\S+)?
    token = ' ' + token + ' '
    return re.sub("https?://\S+|www\.\S+|\\bgoo\.gl/\w+/?|"
                  "(\w+\.){2,4}([a-z]{2,6})(/\S+)*/?|\w+\.([a-z]{2,6})/(\S+/)*(\S+)?", token, text)


def _add_missing_spaces(text):
    # separate word "can't" into two words: "can", "not"
    text = re.sub(r"can't", 'can not', text)
    # replace each suffix `n't` with separated word `not`
    text = re.sub(r"(?<=\w)n't", ' not', text)
    # separate two sentences
    text = re.sub(r'(?<=\w)(?<!\d)\.(?=\w)(?!\d)', '. ', text)
    return text


def _remove_unnecessary_symbols(text):
    text = re.sub("[^\w.!?]+", ' ', text)
    return text


def _replace_key_words(tokens):
    keys = [i for i in repl.keys()]
    for t in tokens:
        if t in keys:
            t = repl[t]
    return tokens
