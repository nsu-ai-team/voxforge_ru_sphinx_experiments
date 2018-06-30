#!/usr/bin/env python
# -*- coding: utf-8 -*-

from argparse import ArgumentParser
import codecs
import os
import sys


def replace_language_model(src):
    if src.startswith(u'$CFG_LANGUAGEMODEL'):
        return u'$CFG_LANGUAGEMODEL  = "$CFG_LIST_DIR/$CFG_DB_NAME.lm";'
    if src.startswith(u'$DEC_CFG_LANGUAGEMODEL'):
        return u'$DEC_CFG_LANGUAGEMODEL  = "$CFG_BASE_DIR/etc/${CFG_DB_NAME}.lm.bin";'
    return src


def main():
    parser = ArgumentParser()
    parser.add_argument('-s', '--src', dest='src_file', type=str, required=True,
                        help='A source file with the CMU Sphinx configuration.')
    parser.add_argument('-d', '--dst', dest='dst_file', type=str, required=True,
                        help='A destination file with the CMU Sphinx configuration.')
    args = parser.parse_args()

    source_file_name = os.path.normpath(args.src_file)
    assert os.path.isfile(source_file_name), u'File "{0}" does not exist!'.format(source_file_name)
    destination_file_name = os.path.normpath(args.dst_file)
    destination_file_dir = os.path.dirname(destination_file_name)
    if len(destination_file_dir) > 0:
        assert os.path.isdir(destination_file_dir), u'Directory "{0}" does not exist!'.format(destination_file_dir)

    with codecs.open(source_file_name, mode='r', encoding='utf-8', errors='ignore') as src_fp:
        source_lines = list(map(lambda it: it.strip(), src_fp.readlines()))

    prepared_lines = list(map(replace_language_model, source_lines))
    with codecs.open(destination_file_name, mode='w', encoding='utf-8', errors='ignore') as dst_fp:
        for cur in prepared_lines:
            dst_fp.write(u'{0}\n'.format(cur))


if __name__ == '__main__':
    main()
