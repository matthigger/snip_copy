from snip_copy.parse import *

text = """ this text
is across
#! snip-start: a
many lines and 
periodically
#! snip-end

contains some command
#! snip-start: a, b
notice that we don't actually include a snip-end here
"""

line_list_expect = [' this text', 'is across', 'many lines and ',
                    'periodically', '', 'contains some command',
                    "notice that we don't actually include a snip-end here",
                    '']
cmd_list_expect = [Command(type='snip-start', line_idx=2, args=['a']),
                   Command(type='snip-end', line_idx=4, args=None),
                   Command(type='snip-start', line_idx=6, args=['a', 'b'])]


def test_parse():
    line_list, cmd_list = parse_text(text=text, cmd_start='#!', cmd_split=':')

    assert line_list == line_list_expect
    assert cmd_list == cmd_list_expect
