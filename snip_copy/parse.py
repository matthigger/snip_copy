from collections import namedtuple
import re

SNIP_START = 'snip'
SNIP_END = 'snip-end'
cmd_tuple = SNIP_END, SNIP_START
Command = namedtuple('Command', ['type', 'line_idx', 'args'])


def parse_text(text, regex_cmd='# ?!', split_cmd=':'):
    """ parses all commands found in file

    Args:
        text (str): input text
        regex_cmd (str): indicates start of command
        split_cmd (str): indicates start of command arguments

    Returns:
        line_list (list): a list of lines which don't contain any commands
        cmd_list (list): a list of commands, in order found in the file
    """

    line_list = str(text).split('\n')

    cmd_list = list()

    line_idx = 0
    while len(line_list) > line_idx:
        # see if line contains a command
        line = line_list[line_idx]
        match = re.search(regex_cmd, line)
        if match is None:
            # line does not contain command, continue searching
            line_idx += 1
            continue

        # remove line (it contains command)
        line_list.pop(line_idx)

        # keep only what remains after cmd_start in line
        _line = line[match.end():]

        # parse & record command
        n_split = _line.count(split_cmd)
        if n_split == 0:
            # no arguments given
            cmd = _line
            args = None
        elif n_split == 1:
            # arguments given
            cmd, arg_csv = _line.split(split_cmd)
            args = [arg.strip() for arg in arg_csv.split(',')]
        else:
            raise SyntaxError('multiple command splits found')
        cmd = cmd.strip()
        assert cmd in cmd_tuple, f'invalid command found on line {line_idx}: {line}'
        cmd_list.append(Command(type=cmd,
                                line_idx=line_idx,
                                args=args))

    return line_list, cmd_list
