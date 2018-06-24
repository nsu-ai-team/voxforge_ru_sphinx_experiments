#!/usr/bin/env python
# -*- coding: utf-8 -*-

import codecs
import os


def check_transcriptions_in_directory(dir_name):
    russian_letters = set(u'АаБбВвГгДдЕеЁёЖжЗзИиЙйКкЛлМмНнОоПпРрСсТтУуФфХхЦцЧчШшЩщЪъЫыЬьЭэЮюЯя')
    consonants = set(u'бвгджзйклмнпрстфхцчшщьъБВГДЖЗЙКЛМНПРСТФХЦЧШЩЬЪ')
    for transcription_file_name in map(lambda it1: os.path.join(dir_name, it1),
                                       filter(lambda it2: it2.lower().endswith('.transcription'),
                                              os.listdir(dir_name))):
        with codecs.open(transcription_file_name, mode='r', encoding='utf-8', errors='ignore') as fp:
            cur_line = fp.readline()
            while len(cur_line) > 0:
                prep_line = cur_line.strip()
                if len(prep_line) > 0:
                    for cur_word in prep_line.split():
                        word_letters = set(cur_word)
                        if word_letters <= russian_letters:
                            if ((len(word_letters) == 1) or (word_letters <= consonants)) and (len(cur_word) > 1):
                                print(u'')
                                print(cur_word)
                                print(prep_line)
                cur_line = fp.readline()
    for subdir_name in filter(lambda it2: os.path.isdir(it2) and (not it2.endswith('.')),
                              map(lambda it1: os.path.join(dir_name, it1), os.listdir(dir_name))):
        check_transcriptions_in_directory(subdir_name)


if __name__ == '__main__':
    check_transcriptions_in_directory(os.path.join(os.path.dirname(__file__), 'etc'))

