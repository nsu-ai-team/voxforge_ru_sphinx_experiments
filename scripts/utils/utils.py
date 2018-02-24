import codecs
import copy
from difflib import SequenceMatcher
import math
import typing


def get_prompt(prompts_name: str, sound_name: str) -> str:
    text = None
    with codecs.open(prompts_name, mode='r', encoding='utf-8', errors='ignore') as fp:
        cur_line = fp.readline()
        while len(cur_line) > 0:
            prepared_line = cur_line.strip()
            if len(prepared_line) > 0:
                tokens = list(filter(
                    lambda it1: len(it1) > 0,
                    map(lambda it2: it2.strip(), prepared_line.lower().split())
                ))
                assert len(tokens) > 1, 'File "{0}": line "{1}" is wrong!'.format(prompts_name, prepared_line)
                if sound_name.lower() == tokens[0]:
                    text = ' '.join(tokens[1:])
                    break
            cur_line = fp.readline()
    assert text is not None, 'File "{0}": sound "{1}" is not found!'.format(prompts_name, sound_name)
    text = text.replace('+', '')
    text = text.replace('.', ' ')
    text = text.replace('!', ' ')
    text = text.replace('?', ' ')
    text = text.replace(',', ' <sil> ')
    text = text.replace(';', ' <sil> ')
    text = text.replace(':', ' <sil> ')
    text = text.replace(' - ', ' <sil> ')
    tokens = text.split()
    assert len(tokens) > 0, 'File "{0}": sound "{1}" contains wrong annotation!'.format(prompts_name, sound_name)
    prepared_tokens = [tokens[0]]
    for cur in tokens[1:]:
        if (cur == '<sil>') and (prepared_tokens[-1] == '<sil>'):
            continue
        prepared_tokens.append(cur)
    assert len(prepared_tokens) > 0, \
        'File "{0}": sound "{1}" contains wrong annotation!'.format(prompts_name, sound_name)
    if len(prepared_tokens) == 1:
        assert prepared_tokens[0] != '<sil>', \
            'File "{0}": sound "{1}" contains wrong annotation!'.format(prompts_name, sound_name)
    return ' '.join(prepared_tokens)


def calc_str_dist(str1: str, str2: str) -> float:
    s = SequenceMatcher(None, str1, str2)
    return 1.0 - s.ratio()


def find_best(subphrases: tuple, tokens: tuple, matches: tuple=None) -> typing.Tuple[float, tuple]:
    if (len(subphrases) == 0) and (len(tokens) == 0):
        return 0.0, matches
    if (len(subphrases) == 0) or (len(tokens) == 0):
        return math.inf, matches
    best_matches = None
    best_dist = None
    n_tokens_in_subphrase = len(subphrases[0].split())
    if n_tokens_in_subphrase <= len(tokens):
        if subphrases[0] == ' '.join(tokens[0:n_tokens_in_subphrase]):
            n = n_tokens_in_subphrase
            next_distance, new_matches = find_best(
                subphrases[1:],
                tokens[n:],
                tuple(tokens[0:n]) if matches is None else (matches + ('<sil>',) + tuple(tokens[0:n]))
            )
            if math.isfinite(next_distance):
                return next_distance, new_matches
    start = max(1, n_tokens_in_subphrase - 2)
    if len(tokens) < start:
        start = len(tokens)
        end = len(tokens) + 1
    else:
        end = min(len(tokens), n_tokens_in_subphrase + 2) + 1
    for n in range(start, end):
        distance = calc_str_dist(subphrases[0], ' '.join(tokens[0:n]))
        next_distance, new_matches = find_best(
            subphrases[1:],
            tokens[n:],
            tuple(tokens[0:n]) if matches is None else (matches + ('<sil>',) + tuple(tokens[0:n]))
        )
        if math.isfinite(next_distance):
            distance += next_distance
        else:
            distance = math.inf
        if best_matches is None:
            best_dist = distance
            best_matches = copy.copy(new_matches)
        else:
            if distance < best_dist:
                best_dist = distance
                best_matches = copy.copy(new_matches)
    return best_dist, best_matches


def combine_texts(text_with_sil: str, text_without_sil: str) -> str:
    parts = tuple(filter(lambda it2: len(it2) > 0, map(lambda it1: it1.strip(), text_with_sil.split('<sil>'))))
    if len(parts) < 2:
        return text_without_sil
    old_tokens = tuple(text_without_sil.split())
    try:
        res, new_tokens = find_best(parts, old_tokens)
        if not math.isfinite(res):
            new_tokens = None
    except:
        new_tokens = None
    assert new_tokens is not None, '"{0}" and "{1}" cannot be combined!'.format(text_with_sil, text_without_sil)
    return ' '.join(new_tokens)