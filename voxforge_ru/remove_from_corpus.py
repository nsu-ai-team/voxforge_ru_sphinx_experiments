#!/usr/bin/env python
# -*- coding: utf-8 -*-

import codecs
import os
import re
import sys


def remove_from_corpus_in_directory(names_of_removed_sounds):
    dir_name = os.path.join(os.path.dirname(__file__), 'etc')
    re_for_sound_name = re.compile(r'\(\S+\)$')
    for subdir_name in filter(lambda it2: os.path.isdir(it2),
                              map(lambda it1: os.path.join(dir_name, it1),
                                  filter(lambda it3: it3.isdigit(), os.listdir(dir_name)))):
        for transcription_file_name in map(lambda it1: os.path.join(subdir_name, it1),
                                           filter(lambda it2: it2.lower().endswith('.transcription'),
                                                  os.listdir(subdir_name))):
            line_idx = 1
            saved_lines = []
            n_lines = 0
            with codecs.open(transcription_file_name, mode='r', encoding='utf-8', errors='ignore') as fp:
                cur_line = fp.readline()
                while len(cur_line) > 0:
                    prep_line = cur_line.strip()
                    if len(prep_line) > 0:
                        n_lines += 1
                        err_msg = u'File "{0}": line {1} is wrong!'.format(transcription_file_name, line_idx)
                        search_res = re_for_sound_name.search(prep_line)
                        assert search_res is not None, err_msg
                        assert (search_res.start() >= 0) and (search_res.end() >= 0), err_msg
                        if prep_line[(search_res.start() + 1):(search_res.end() - 1)] not in names_of_removed_sounds:
                            saved_lines.append(prep_line)
                    cur_line = fp.readline()
                    line_idx += 1
            if len(saved_lines) == 0:
                print(u'File "{0}": all lines were been removed.'.format(transcription_file_name))
            elif (n_lines - len(saved_lines)) == 0:
                print(u'File "{0}": no lines were been removed.'.format(transcription_file_name))
            elif (n_lines - len(saved_lines)) == 1:
                print(u'File "{0}": 1 line was been removed.'.format(transcription_file_name))
            else:
                print(u'File "{0}": {1} lines were been removed.'.format(transcription_file_name, n_lines - len(saved_lines)))
            if (n_lines - len(saved_lines)) > 0:
                with codecs.open(transcription_file_name, mode='w', encoding='utf-8', errors='ignore') as fp:
                    for cur in saved_lines:
                        fp.write(u'{0}\n'.format(cur))
        for fileids_file_name in map(lambda it1: os.path.join(subdir_name, it1),
                                     filter(lambda it2: it2.lower().endswith('.fileids'), os.listdir(subdir_name))):
            line_idx = 1
            saved_lines = []
            n_lines = 0
            with codecs.open(fileids_file_name, mode='r', encoding='utf-8', errors='ignore') as fp:
                cur_line = fp.readline()
                while len(cur_line) > 0:
                    prep_line = cur_line.strip()
                    if len(prep_line) > 0:
                        n_lines += 1
                        if prep_line not in names_of_removed_sounds:
                            saved_lines.append(prep_line)
                    cur_line = fp.readline()
                    line_idx += 1
            if len(saved_lines) == 0:
                print(u'File "{0}": all lines were been removed.'.format(fileids_file_name))
            elif (n_lines - len(saved_lines)) == 0:
                print(u'File "{0}": no lines were been removed.'.format(fileids_file_name))
            elif (n_lines - len(saved_lines)) == 1:
                print(u'File "{0}": 1 line was been removed.'.format(fileids_file_name))
            else:
                print(u'File "{0}": {1} lines were been removed.'.format(fileids_file_name, n_lines - len(saved_lines)))
            if (n_lines - len(saved_lines)) > 0:
                with codecs.open(fileids_file_name, mode='w', encoding='utf-8', errors='ignore') as fp:
                    for cur in saved_lines:
                        fp.write(u'{0}\n'.format(cur))
    

if __name__ == '__main__':
    assert len(sys.argv) > 1, 'There are no files for removing!'
    files_for_removing = []
    for ind in range(1, len(sys.argv)):
        new_file_name = sys.argv[ind].strip()
        if len(new_file_name) > 0:
            files_for_removing.append(new_file_name)
    assert len(files_for_removing) > 0, 'There are no files for removing!'
    remove_from_corpus_in_directory(set(files_for_removing))

