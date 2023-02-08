from collections import namedtuple
import re

SNIP_START = 'snip-start'
SNIP_END = 'snip-end'
cmd_tuple = SNIP_END, SNIP_START
Command = namedtuple('Command', ['type', 'line_idx', 'args'])


def parse_text(text, cmd_start='# ?!', cmd_split=':'):
    """ parses all commands found in file

    Args:
        text (str): input text
        cmd_start (str): indicates start of command
        cmd_split (str): indicates start of command arguments

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
        match = re.search(cmd_start, line)
        if match is None:
            # line does not contain command, continue searching
            line_idx += 1
            continue

        # remove line (it contains command)
        line_list.pop(line_idx)

        # keep only what remains after cmd_start in line
        line = line[match.end():]

        # parse & record command
        n_split = line.count(cmd_split)
        if n_split == 0:
            # no arguments given
            cmd = line
            args = None
        elif n_split == 1:
            # arguments given
            cmd, arg_csv = line.split(cmd_split)
            args = [arg.strip() for arg in arg_csv.split(',')]
        else:
            raise SyntaxError('multiple command splits found')
        cmd = cmd.strip()
        assert cmd in cmd_tuple, f'invalid command: {cmd}'
        cmd_list.append(Command(type=cmd,
                                line_idx=line_idx,
                                args=args))

    return line_list, cmd_list