#!/usr/bin/env python
# -*- coding: utf-8 -*-

import codecs
import os


def get_mfc_list():
    feat_dir = os.path.join(os.path.dirname(__file__), 'feat')
    if not os.path.isdir(feat_dir):
        raise ValueError('The directory "{0}" does not exist!'.format(feat_dir))
    speakers = list(filter(
        lambda it: (it not in {'.', '..'}) and os.path.isdir(os.path.join(feat_dir, it)), os.listdir(feat_dir)
    ))
    if len(speakers) == 0:
        raise ValueError('There are no speakers!')
    mfc_list = []
    for cur_speaker in speakers:
        wav_subdir = os.path.join(feat_dir, cur_speaker, 'wav')
        if not os.path.isdir(wav_subdir):
            raise ValueError('The directory "{0}" does not exist!'.format(wav_subdir))
        sounds = list(filter(
            lambda it: it.lower().endswith('.mfc') and (len(it) > 4) and (len(it.strip()) == len(it)),
            os.listdir(wav_subdir)
        ))
        if len(sounds) == 0:
            raise ValueError('There are no *.mfc files in the directory "{0}".'.format(wav_subdir))
        for cur_sound in sounds:
            mfc_list.append(cur_speaker + '/wav/' + cur_sound[:-4])
    return set(mfc_list)


def read_fileids(dir_name):
    all_files = list(filter(
        lambda it: it.lower().endswith('.fileids') and os.path.isfile(os.path.join(dir_name, it)),
        os.listdir(dir_name)
    ))
    if len(all_files) != 2:
        raise ValueError('The directory "{0}" contains wrong *.fileids!'.format(dir_name))
    if set(all_files) != {'voxforge_ru_test.fileids', 'voxforge_ru_train.fileids'}:
        raise ValueError('The directory "{0}" contains wrong *.fileids!'.format(dir_name))
    soundlist = set()
    for cur in map(lambda it: os.path.join(dir_name, it), all_files):
        with codecs.open(cur, mode='r', encoding='utf-8', errors='ignore') as fp:
            curline = fp.readline()
            while len(curline) > 0:
                prepline = curline.strip()
                if len(prepline) > 0:
                    if prepline in soundlist:
                        raise ValueError('File "{0}": sound {1} is duplicated!'.format(cur, prepline))
                    soundlist.add(prepline)
                curline = fp.readline()
    return soundlist


def get_all_subdirs():
    etc_dir = os.path.join(os.path.dirname(__file__), 'etc')
    assert os.path.isdir(etc_dir)
    subdirs = list(filter(lambda it: it.isdigit() and os.path.isdir(os.path.join(etc_dir, it)), os.listdir(etc_dir)))
    if len(subdirs) == 0:
        raise ValueError('There are no sub-directories!')
    subdirs.sort(key=lambda it: int(it))
    if (subdirs[0] != '1') or (subdirs[-1] != '{0}'.format(len(subdirs))):
        raise ValueError('{0} is incorrect list of sub-directories!'.format(subdirs))
    return [os.path.join(etc_dir, it) for it in subdirs]


if __name__ == '__main__':
    set_of_mfc_files = get_mfc_list()
    list_of_subdirs = get_all_subdirs()
    set_of_sounds = read_fileids(list_of_subdirs[0])
    for cur_subdir in list_of_subdirs[1:]:
        if read_fileids(cur_subdir) != set_of_sounds:
            raise ValueError('The sub-directory "{0}" contains different information in *.fileids!'.format(cur_subdir))
    list_of_unknown_sounds = sorted(list(set_of_sounds - set_of_mfc_files))
    if len(list_of_unknown_sounds) > 0:
        for it in list_of_unknown_sounds:
            print it
