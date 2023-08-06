#!/usr/bin/env python
# -*-coding:utf-8-*-


import logging
import heapq
from math import log
from .utils import is_empty_string

logger = logging.getLogger(__name__)

"""
将一篇文章按照句子或者段落分开，然后进行tf-idf评分。

word(tf) = Cword(target word count in sent)/C(all word count in sent)

word(idf) = log(C(sent count)/C(target word in sent count))

"""


def is_word_passed(word, stop_words):
    if word in stop_words:
        return True
    elif is_empty_string(word):
        return True
    else:
        return False


def calc_word_frequencies(word_list, stop_words):
    word_frequencies = {}
    for word in word_list:
        if not is_word_passed(word, stop_words):
            if word not in word_frequencies.keys():
                word_frequencies[word] = 1
            else:
                word_frequencies[word] += 1

    return word_frequencies


def auto_summary(content, word_tokenizer=None, sent_tokenizer=None,
                 stop_words=None, max_len=50):
    if stop_words is None:
        from .chinese_stop_words import STOP_WORDS
        stop_words = STOP_WORDS
    if sent_tokenizer is None:
        from .tokenize import ChineseSentenceTokenizer
        sent_tokenizer = ChineseSentenceTokenizer()
    if word_tokenizer is None:
        from fenci.segment import Segment
        word_tokenizer = Segment()

    sentence_list = sent_tokenizer.tokenize(content)

    sent_count = len(sentence_list)
    word_in_sent = {}

    for sent_index, sent in enumerate(sentence_list):
        word_list = word_tokenizer.tokenize(sent)

        for word in word_list:
            if not is_word_passed(word, stop_words):
                if word in word_in_sent:
                    word_in_sent[word].add(sent_index)
                else:
                    word_in_sent[word] = {sent_index}

    sentence_scores = {}
    for sent_index, sent in enumerate(sentence_list):
        word_list = word_tokenizer.tokenize(sent)
        all_word_count = len(word_list)
        word_frequencies = calc_word_frequencies(word_list, stop_words)

        for word in word_list:
            if not is_word_passed(word, stop_words):
                word_tf = word_frequencies[word] / all_word_count
                word_idf = log(sent_count / len(word_in_sent[word]), 10)

                word_tf_idf = word_tf * word_idf

                if sent_index in sentence_scores:
                    sentence_scores[sent_index] += word_tf_idf
                else:
                    sentence_scores[sent_index] = word_tf_idf

    summary_sentences = heapq.nlargest(max_len, sentence_scores,
                                       key=sentence_scores.get)

    # 继续保证文本顺序
    result = []
    for i in sorted(summary_sentences):
        result.append(sentence_list[i])

    return result
