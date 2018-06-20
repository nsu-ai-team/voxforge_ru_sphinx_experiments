#!/usr/bin/env python
# -*- coding: utf-8 -*-

from argparse import ArgumentParser
import codecs
import copy
import os
import re
import warnings


def read_ruscorpora_ngrams(file_name):
    ngrams = dict()
    line_index = 1
    re_for_word = re.compile(r'(\w+|\w+[\w\-]*\w+)', re.U)
    re_for_split = re.compile(r'\s+', re.U)
    re_for_digits = re.compile(r'\d+', re.U)
    russian_letters = set(u'абвгдеёжзийклмнопрстуфхцчшщъыьэюя-')
    with codecs.open(file_name, mode='r', encoding='utf-8', errors='ignore') as fp:
        cur_line = fp.readline()
        while len(cur_line) > 0:
            prep_line = cur_line.strip().lower()
            if len(prep_line) > 0:
                err_msg = 'File "{0}", line {1} is wrong!'.format(file_name, line_index)
                line_parts = tuple(
                    filter(
                        lambda it2: len(it2) > 0,
                        map(
                            lambda it1: it1.strip(),
                            re_for_split.split(prep_line)
                        )
                    )
                )
                assert len(line_parts) >= 2, err_msg
                assert line_parts[0].isdigit(), err_msg
                ngram_frequency = int(line_parts[0])
                ngram_parts = tuple(filter(lambda it: re_for_word.search(it) is not None, line_parts[1:]))
                if len(ngram_parts) > 0:
                    if re_for_digits.search(' '.join(ngram_parts)) is None:
                        set_of_letters = set(''.join(ngram_parts))
                        if (set_of_letters <= russian_letters) and (set_of_letters != {u'-'}):
                            ngrams[ngram_parts] = ngram_frequency + ngrams.get(ngram_parts, 0)
                else:
                    warnings.warn(err_msg)
            cur_line = fp.readline()
            line_index += 1
    return ngrams


def unite_ngrams(list_of_ngrams):
    united_ngrams = copy.deepcopy(list_of_ngrams[0])
    for ngrams in list_of_ngrams[1:]:
        for cur_ngram in ngrams:
            united_ngrams[cur_ngram] = ngrams[cur_ngram] + united_ngrams.get(cur_ngram, 0)
    return united_ngrams


def write_ngrams_for_srilm(ngrams, file_name):
    with codecs.open(file_name, mode='w', encoding='utf-8', errors='ignore') as fp:
        for cur_ngram in sorted(ngrams.keys()):
            fp.write(u'{0} {1}\n'.format(' '.join(cur_ngram), ngrams[cur_ngram]))


def write_vocabulary_for_srilm(ngrams, file_name):
    all_words = set()
    for cur_ngram in ngrams:
        all_words |= set(cur_ngram)
    with codecs.open(file_name, mode='w', encoding='utf-8', errors='ignore') as fp:
        for cur_word in sorted(all_words):
            fp.write(u'{0}\n'.format(cur_word))


def main():
    parser = ArgumentParser()
    parser.add_argument('-s', '--src', dest='src_dir', type=str, required=True,
                        help='A source directory with RusCorpora n-grams as text files.')
    parser.add_argument('-d', '--dst', dest='dst_file', type=str, required=True,
                        help='A destination text file with n-grams which are prepared for SRILM.')
    parser.add_argument('-t', '--type', dest='result_type', help='Type of result: vocabulary of n-grams.',
                        choices=['ngrams', 'vocabulary'], required=True)
    args = parser.parse_args()

    source_dir_name = os.path.normpath(args.src_dir)
    assert os.path.isdir(source_dir_name), u'Directory "{0}" does not exist!'.format(source_dir_name)
    destination_file_name = os.path.normpath(args.dst_file)
    destination_file_dir = os.path.dirname(destination_file_name)
    if len(destination_file_dir) > 0:
        assert os.path.isdir(destination_file_dir), u'Directory "{0}" does not exist!'.format(destination_file_dir)

    all_source_files = [os.path.join(source_dir_name, cur_name)
                        for cur_name in filter(lambda it: it.lower().endswith('.txt'), os.listdir(source_dir_name))]
    assert len(all_source_files) > 0, u'There are no text files in the directory "{0}".'.format(source_dir_name)

    ngrams = unite_ngrams([read_ruscorpora_ngrams(cur_name) for cur_name in all_source_files])
    if args.result_type == 'ngrams':
        write_ngrams_for_srilm(ngrams, destination_file_name)
    else:
        write_vocabulary_for_srilm(ngrams, destination_file_name)


if __name__ == '__main__':
    main()
