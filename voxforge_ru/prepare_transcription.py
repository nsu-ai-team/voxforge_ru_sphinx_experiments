from argparse import ArgumentParser
import codecs
import os


def main():
    parser = ArgumentParser()
    parser.add_argument('-d', '--dict', dest='dictionary', type=str, required=True,
                        help='Name of phonetic dictionary.')
    parser.add_argument('-t', '--trans', dest='transcription', type=str, required=True,
                        help='Name of transcriptions list.')
    args = parser.parse_args()

    dictionary = dict()
    with codecs.open(os.path.normpath(args.dictionary), mode='r', encoding='utf-8', errors='ignore') as fp:
        cur_line = fp.readline()
        while len(cur_line) > 0:
            prep_line = cur_line.strip()
            if len(prep_line) > 0:
                parts = prep_line.split()
                assert len(parts) >= 2
                word = parts[0]
                transcription = ' '.join(parts[1:])
                if word not in dictionary:
                    dictionary[word] = transcription
            cur_line = fp.readline()
    
    texts = list()
    with codecs.open(os.path.normpath(args.transcription), mode='r', encoding='utf-8', errors='ignore') as fp:
        cur_line = fp.readline()
        while len(cur_line) > 0:
            prep_line = cur_line.strip()
            if len(prep_line) > 0:
                found_pos = prep_line.find('(')
                assert found_pos > 0
                words = prep_line[:found_pos].strip().split()
                processed_words = [dictionary.get(cur, cur) for cur in words]
                texts.append(' '.join(processed_words) + ' ' + prep_line[found_pos:])
            cur_line = fp.readline()
    with codecs.open(os.path.normpath(args.transcription), mode='w', encoding='utf-8', errors='ignore') as fp:
        for cur in texts:
            fp.write('{0}\n'.format(cur))


if __name__ == '__main__':
    main()
