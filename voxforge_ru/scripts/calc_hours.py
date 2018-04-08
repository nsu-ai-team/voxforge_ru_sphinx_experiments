from argparse import ArgumentParser
import os

from scipy.io.wavfile import read


def get_hours_of_sound(sound_name: str) -> float:
    fs, data = read(sound_name)
    assert fs == 8000, 'Sound "{0}": sample rate as wrong! {1} <> 8000'.format(sound_name, fs)
    seconds = data.shape[0] / float(fs)
    return seconds / 3600.0


def main():
    parser = ArgumentParser()
    parser.add_argument('-s', '--sounds', dest='sounds_dir', type=str, required=True,
                        help='Name of directory with sound files.')
    args = parser.parse_args()

    sounds_dir_name = os.path.normpath(args.sounds_dir)
    assert os.path.isdir(sounds_dir_name), "Directory \"{0}\" does not exist!".format(sounds_dir_name)
    names_of_sound_files = list(filter(lambda it: it.lower().endswith('.wav'), os.listdir(sounds_dir_name)))
    assert len(names_of_sound_files), 'There are no sound files in the directory "{0}"!'.format(sounds_dir_name)
    total_duration = 0.0
    for cur_name in names_of_sound_files:
        total_duration += get_hours_of_sound(os.path.join(sounds_dir_name, cur_name))
    hours = int(total_duration)
    eps = 1e-9
    if (total_duration - hours) > eps:
        minutes = int((total_duration - hours) * 60.0)
        if (total_duration - hours - 60 * minutes) > eps:
            seconds = total_duration - hours - 60 * minutes
        else:
            seconds = 0.0
    else:
        minutes = 0
        seconds = 0.0
    print('{0} hours {1} minutes {2:.3f} seconds'.format(hours, minutes, seconds))


if __name__ == '__main__':
    main()
