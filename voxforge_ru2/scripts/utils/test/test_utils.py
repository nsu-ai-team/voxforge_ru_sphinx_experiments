import os
import re
import unittest

from utils import get_prompt, combine_texts


class TestUtils(unittest.TestCase):
    def setUp(self):
        self.prompts_name = os.path.join(os.path.split(__file__)[0], 'testdata', 'prompts-original')

    def test_get_prompt_positive01(self):
        target_sound = 'ru_0022'
        true_text = 'над этой машиной <sil> он ткнул трубкой в сторону лесов <sil> работаю давно'
        loaded_text = get_prompt(self.prompts_name, target_sound)
        self.assertEqual(true_text, loaded_text)

    def test_get_prompt_positive02(self):
        target_sound = 'len_ru_0299'
        true_text = 'у него было ко мне хорошее отношение'
        loaded_text = get_prompt(self.prompts_name, target_sound)
        self.assertEqual(true_text, loaded_text)

    def test_get_prompt_positive03(self):
        target_sound = 'ru_0006'
        true_text = 'глаза ленивые <sil> серо-карие <sil> и так же как у той женщины <sil> с искоркой'
        loaded_text = get_prompt(self.prompts_name, target_sound)
        self.assertEqual(true_text, loaded_text)

    def test_get_prompt_negative_01(self):
        target_sound = 'ru_0007'
        true_err_msg = re.escape('File "{0}": sound "{1}" is not found!'.format(self.prompts_name, target_sound))
        with self.assertRaisesRegex(AssertionError, true_err_msg):
            _ = get_prompt(self.prompts_name, target_sound)

    def test_get_prompt_negative_02(self):
        target_sound = 'bad_text_1'
        true_err_msg = re.escape('File "{0}": sound "{1}" contains wrong annotation!'.format(
            self.prompts_name, target_sound
        ))
        with self.assertRaisesRegex(AssertionError, true_err_msg):
            print(get_prompt(self.prompts_name, target_sound))

    def test_get_prompt_negative_03(self):
        target_sound = 'bad_text_2'
        true_err_msg = re.escape('File "{0}": sound "{1}" contains wrong annotation!'.format(
            self.prompts_name, target_sound
        ))
        with self.assertRaisesRegex(AssertionError, true_err_msg):
            print(get_prompt(self.prompts_name, target_sound))

    def test_combine_texts_positive_01(self):
        text_with_sil = 'aaa bbb ccc <sil> dd34 <sil> в'
        text_without_sil = 'a1a bbb csc dd34 u'
        true_text = 'a1a bbb csc <sil> dd34 <sil> u'
        calculated_text = combine_texts(text_with_sil, text_without_sil)
        self.assertEqual(true_text, calculated_text)

    def test_combine_texts_positive_02(self):
        text_with_sil = 'aaa bbb ccc <sil> dd34 <sil> в'
        text_without_sil = 'a1a bbb 3 csc dd34 u'
        true_text = 'a1a bbb 3 csc <sil> dd34 <sil> u'
        calculated_text = combine_texts(text_with_sil, text_without_sil)
        self.assertEqual(true_text, calculated_text)

    def test_combine_texts_positive_03(self):
        text_with_sil = 'aaa bbbccc <sil> dd34 <sil> в'
        text_without_sil = 'a1a bbb 3 csc dd34 u'
        true_text = 'a1a bbb 3 csc <sil> dd34 <sil> u'
        calculated_text = combine_texts(text_with_sil, text_without_sil)
        self.assertEqual(true_text, calculated_text)

    def test_combine_texts_positive_04(self):
        text_with_sil = 'аппарат прорезывал облака над тусклой равниной <sil> и <sil> ревя и сотрясаясь <sil> ' \
                        'медленно теперь опускался садимся <sil> успел только крикнуть лось и выключил двигатель'
        text_without_sil = 'аппарат прорезывал облака над тусклой равниной и ревя и сотрясаясь медленно теперь ' \
                           'опускался садимся успел только крикнуть лось и выключил двигатель'
        true_text = 'аппарат прорезывал облака над тусклой равниной <sil> и <sil> ревя и сотрясаясь <sil> медленно ' \
                    'теперь опускался садимся <sil> успел только крикнуть лось и выключил двигатель'
        calculated_text = combine_texts(text_with_sil, text_without_sil)
        self.assertEqual(true_text, calculated_text)


if __name__ == '__main__':
    unittest.main(verbosity=2)