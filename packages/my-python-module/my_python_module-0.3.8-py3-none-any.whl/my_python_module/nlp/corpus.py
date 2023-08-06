#!/usr/bin/env python
# -*-coding:utf-8-*-

from nltk.corpus import PlaintextCorpusReader
from .tokenize import ChineseSentenceTokenizer
from my_python_module.nlp.text import ChineseText
from fenci.segment import Segment

def load_corpus(root, word_tokenizer=Segment(),
                sent_tokenizer=ChineseSentenceTokenizer()):
    return PlaintextCorpusReader(root, r"(?!\.).*\.txt",
                                 word_tokenizer=word_tokenizer,
                                 sent_tokenizer=sent_tokenizer,
                                 encoding='utf8')


zh_gutenberg = load_corpus('D:/nlp_data/corpora/zh_gutenberg')

laozi = ChineseText(zh_gutenberg.words("laozi_s.txt"))
lunyu = ChineseText(zh_gutenberg.words("lunyu_s.txt"))
xiyouji = ChineseText(zh_gutenberg.words("xiyouji_s.txt"))
# hongloumeng = ChineseText(zh_gutenberg.words("hongloumeng_s.txt"))
# shuihuzhuan = ChineseText(zh_gutenberg.words("shuihuzhuan_s.txt"))
# sanguoyanyi = ChineseText(zh_gutenberg.words("sanguoyanyi_s.txt"))
# guwenguanzhi = ChineseText(zh_gutenberg.words("guwenguanzhi_s.txt"))
