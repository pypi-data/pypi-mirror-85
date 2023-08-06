#!/usr/bin/env python
# -*-coding:utf-8-*-


from nltk.text import Text, BigramCollocationFinder, BigramAssocMeasures, \
    tokenwrap


class ChineseText(Text):

    def collocation_list(self, num=20, window_size=2):
        """
        Return collocations derived from the text, ignoring stopwords.

            >>> from nltk.book import text4
            >>> text4.collocation_list()[:2]
            [('United', 'States'), ('fellow', 'citizens')]

        :param num: The maximum number of collocations to return.
        :type num: int
        :param window_size: The number of tokens spanned by a collocation (default=2)
        :type window_size: int
        :rtype: list(tuple(str, str))
        """
        if not (
                "_collocations" in self.__dict__
                and self._num == num
                and self._window_size == window_size
        ):
            self._num = num
            self._window_size = window_size

            from .chinese_stop_words import STOP_WORDS

            finder = BigramCollocationFinder.from_words(self.tokens,
                                                        window_size)
            finder.apply_freq_filter(2)
            finder.apply_word_filter(lambda w: w in STOP_WORDS)
            # 移除空白字符
            from my_python_module.nlp.utils import is_empty_string
            finder.apply_word_filter(lambda w: is_empty_string(w))

            bigram_measures = BigramAssocMeasures()
            self._collocations = list(
                finder.nbest(bigram_measures.likelihood_ratio, num))
        return self._collocations
