import pathlib

from snip_copy.copy import *

folder = pathlib.Path('.') / 'ex_hw'
text_dict = dict()
for file in folder.glob('*.py'):
    with open(file) as f:
        text_dict[file.stem] = f.read()


def test_snip_copy():
    suffix_text_dict = snip_copy(text_dict['rubric'])

    assert text_dict['solution'] == suffix_text_dict['solution']
    assert text_dict['student'] == suffix_text_dict['student']
