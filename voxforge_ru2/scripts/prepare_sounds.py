from argparse import ArgumentParser
import codecs
import csv
import os
import re
import random
import shutil

from utils import get_prompt, combine_texts


def load_sound_names(base_dir: str, csv_file_name: str, add_silences: bool) -> list:
    sounds_by_speakers = dict()
    line_index = 1
    with codecs.open(csv_file_name, mode='r', encoding='utf-8', errors='ignore') as fp:
        csv_reader = csv.reader(fp, delimiter=',', quotechar='"')
        for cur_row in csv_reader:
            if (line_index % 500) == 0:
                print('We have been processed {0} lines...'.format(line_index))
            if len(cur_row) > 0:
                err_msg = 'File "{0}": line {1} is wrong!'.format(csv_file_name, line_index)
                assert len(cur_row) == 3, err_msg
                file_name = cur_row[0]
                file_path, base_name = os.path.split(file_name)
                assert (len(file_path) > 0) and (len(base_name) > 0), err_msg
                speaker_dir, wav_path = os.path.split(file_path)
                assert (len(speaker_dir) > 0) and (wav_path == 'wav'), err_msg
                right_annotated_text = ' '.join(list(filter(
                    lambda it: (len(it) > 0) and (it != 'sil') and (it != '<sil>'),
                    cur_row[1].lower().split()
                )))
                assert len(right_annotated_text) > 0, err_msg
                if add_silences:
                    prompts_name = os.path.join(base_dir, speaker_dir, 'etc', 'prompts-original')
                    annotated_text = combine_texts(get_prompt(prompts_name, base_name), right_annotated_text)
                else:
                    annotated_text = right_annotated_text
                assert len(annotated_text) > 0, err_msg
                if not os.path.isfile(os.path.join(base_dir, file_name)):
                    file_name = cur_row[0] + '.wav'
                    assert os.path.isfile(os.path.join(base_dir, file_name)), err_msg
                found_pos = speaker_dir.find('-')
                if found_pos >= 0:
                    speaker_name = speaker_dir[:found_pos].strip().lower()
                else:
                    speaker_name = speaker_dir.lower()
                assert len(speaker_name) > 0, err_msg
                if speaker_name in sounds_by_speakers:
                    sounds_by_speakers[speaker_name].append((file_name, annotated_text))
                else:
                    sounds_by_speakers[speaker_name] = [(file_name, annotated_text)]
            line_index += 1
    print('We have been processed {0} lines...'.format(line_index))
    print('')
    prepared_sounds_by_speakers = []
    n_all_sounds = 0
    for speaker_name in sounds_by_speakers:
        n_all_sounds += len(sounds_by_speakers[speaker_name])
    for speaker_name in sorted(list(sounds_by_speakers.keys())):
        prepared_sounds_by_speakers.append(
            (
                speaker_name,
                len(sounds_by_speakers[speaker_name]) / float(n_all_sounds),
                tuple(sorted(sounds_by_speakers[speaker_name], key=lambda it: (it[1], it[0])))
            )
        )
    return prepared_sounds_by_speakers


def split_cv(all_sounds: list, cv: int) -> tuple:
    random.shuffle(all_sounds)
    true_part = 1.0 / float(cv)
    sounds_by_folds = list()
    start_ind = 0
    for fold_ind in range(cv - 1):
        assert start_ind < (len(all_sounds) - 1), 'Sounds cannot be splitted!'
        part = 0.0
        found_ind = -1
        for ind in range(start_ind, len(all_sounds)):
            part += all_sounds[ind][1]
            if part >= true_part:
                found_ind = ind
                break
        assert found_ind > start_ind, 'Sounds cannot be splitted!'
        sounds_by_folds.append(tuple(all_sounds[start_ind:(found_ind + 1)]))
        start_ind = found_ind + 1
    assert start_ind < len(all_sounds), 'Sounds cannot be splitted!'
    sounds_by_folds.append(tuple(all_sounds[start_ind:]))
    return tuple(sounds_by_folds)
           

def main():
    parser = ArgumentParser()
    parser.add_argument('-s', '--src', dest='src_dir', type=str, required=True,
                        help='Name of source directory with Voxforge\'s sound files.')
    parser.add_argument('-d', '--dst', dest='dst_dir', type=str, required=True,
                        help='Name of destination directory with sounds for CMU Sphinx.')
    parser.add_argument('-c', '--csv', dest='csv_name', type=str, required=True,
                        help='Name of CSV-file with list of Voxforge\'s sound files.')
    args = parser.parse_args()

    source_dir_name = os.path.normpath(args.src_dir)
    assert os.path.isdir(source_dir_name), "Directory \"{0}\" does not exist!".format(source_dir_name)
    destination_dir_name = os.path.normpath(args.dst_dir)
    assert os.path.isdir(destination_dir_name), "Directory \"{0}\" does not exist!".format(destination_dir_name)
    csv_file_name = os.path.normpath(args.csv_name)
    assert os.path.isfile(csv_file_name), "File \"{0}\" does not exist!".format(csv_file_name)

    all_sound_names = load_sound_names(source_dir_name, csv_file_name, True)
    print('Speakers list:')
    max_speaker_name_size = 0
    for speaker_data in all_sound_names:
        speaker_name = speaker_data[0]
        if len(speaker_name) > max_speaker_name_size:
            max_speaker_name_size = len(speaker_name)
    for speaker_data in sorted(all_sound_names, key=lambda it: it[0]):
        speaker_name = speaker_data[0]
        speaker_part = speaker_data[1]
        print('{0:<{1}} {2:>6.2%}'.format(speaker_name, max_speaker_name_size, speaker_part))
    print('')
    sounds_by_folds = split_cv(all_sound_names, 3)
    re_for_splitting = re.compile(r'[\\/]+')

    base_destination_dir = os.path.split(destination_dir_name)[1]
    assert len(base_destination_dir) > 0, "Directory \"{0}\" is wrong!".format(destination_dir_name)

    for fold_ind in range(len(sounds_by_folds)):
        etc_dir_name = os.path.join(destination_dir_name, '{0}_{1}'.format(base_destination_dir, fold_ind + 1), 'etc')
        assert os.path.isdir(etc_dir_name), "Directory \"{0}\" does not exist!".format(etc_dir_name)
        wav_dir_name = os.path.join(destination_dir_name, '{0}_{1}'.format(base_destination_dir, fold_ind + 1), 'wav')
        assert os.path.isdir(wav_dir_name), "Directory \"{0}\" does not exist!".format(wav_dir_name)
        train_dir_name = os.path.join(wav_dir_name, 'train')
        assert os.path.isdir(train_dir_name), "Directory \"{0}\" does not exist!".format(train_dir_name)
        sounds_for_testing = sounds_by_folds[fold_ind]
        sounds_for_training = []
        for other_fold_ind in range(len(sounds_by_folds)):
            if other_fold_ind == fold_ind:
                continue
            sounds_for_training += sounds_by_folds[other_fold_ind]
        file_ids = None
        file_trans = None
        try:
            file_ids = codecs.open(os.path.join(etc_dir_name, os.path.split(destination_dir_name)[1] + '_train.fileids'),
                                   mode='w', encoding='utf-8', errors='ignore')
            file_trans = codecs.open(os.path.join(etc_dir_name, os.path.split(destination_dir_name)[1] + '_train.transcription'),
                                     mode='w', encoding='utf-8', errors='ignore')
            for speaker_data in sounds_for_training:
                for sound_name in speaker_data[2]:
                    source_file_name = os.path.join(source_dir_name, sound_name[0])
                    base_name = '-'.join(list(filter(
                        lambda it1: (it1.lower() != 'wav') and (len(it1) > 0),
                        map(lambda it2: it2.strip(), re_for_splitting.split(sound_name[0])))
                    ))
                    destination_file_name = os.path.join(
                        train_dir_name,
                        base_name
                    )
                    shutil.copy2(source_file_name, destination_file_name)
                    file_ids.write('train/{0}\n'.format(base_name[:-4]))
                    file_trans.write('<s> {0} </s> ({1})\n'.format(sound_name[1], base_name[:-4]))
        finally:
            if file_ids is not None:
                file_ids.close()
            if file_trans is not None:
                file_trans.close()
        test_dir_name = os.path.join(wav_dir_name, 'test')
        assert os.path.isdir(test_dir_name), "Directory \"{0}\" does not exist!".format(test_dir_name)
        file_ids = None
        file_trans = None
        try:
            file_ids = codecs.open(os.path.join(etc_dir_name, os.path.split(destination_dir_name)[1] + '_test.fileids'),
                                   mode='w', encoding='utf-8', errors='ignore')
            file_trans = codecs.open(os.path.join(etc_dir_name, os.path.split(destination_dir_name)[1] + '_test.transcription'),
                                     mode='w', encoding='utf-8', errors='ignore')
            for speaker_data in sounds_for_testing:
                for sound_name in speaker_data[2]:
                    source_file_name = os.path.join(source_dir_name, sound_name[0])
                    base_name = '-'.join(list(filter(
                        lambda it1: (it1.lower() != 'wav') and (len(it1) > 0),
                        map(lambda it2: it2.strip(), re_for_splitting.split(sound_name[0])))
                    ))
                    destination_file_name = os.path.join(
                        test_dir_name,
                        base_name
                    )
                    shutil.copy2(source_file_name, destination_file_name)
                    file_ids.write('test/{0}\n'.format(base_name[:-4]))
                    file_trans.write('{0} ({1})\n'.format(' '.join(sound_name[1].replace('<sil>', ' ').split()), base_name[:-4]))
        finally:
            if file_ids is not None:
                file_ids.close()
            if file_trans is not None:
                file_trans.close()


if __name__ == '__main__':
    main()

