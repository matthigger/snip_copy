import argparse
import pathlib
from warnings import warn

from snip_copy.copy import snip_copy

description = 'creates copies of a file, snipping away portions of the ' \
              'original.  See https://github.com/matthigger/snip_copy'
parser = argparse.ArgumentParser(prog='snip_copy',
                                 description=description)
parser.add_argument('file_in', type=str, help='input file')
parser.add_argument("--cmd-start", type=str, default='# ?!',
                    help="regex to indicate start of command (e.g. "
                         "'snip-start' or 'snip-end')")


def main(args=None, write_new_file=True):
    """ loads a file, snip copies and optionally writes new file

    (this fnc allows us to test)
    Args:
        args: mimics sys.argv, defaults to actually using sys.argv
        write_new_file (bool): if True, writes new file

    Returns:
        suffix_text_dict (dict): keys are suffixes of different outputs,
            values are str of text snipped per that suffix
    """
    args = parser.parse_args(args=args)

    # read in file
    with open(args.file_in) as f:
        text = f.read()

    # snip and copy to make new files
    suffix_text_dict = snip_copy(text, cmd_start=args.cmd_start)
    # todo: (suffix vs stem?)

    if write_new_file:
        file_in = pathlib.Path(args.file_in)
        for stem, text in suffix_text_dict.items():
            if stem is None:
                # stem is None has text of orig file with commands removed
                continue

            # build (and check) file_out
            file_out = file_in.with_stem(stem)
            if file_in == file_out:
                # skip writing output (overwrites source file)
                warn(f'skipped: output file may not overwrite input '
                     f'({file_in})')
                continue

            # print text to output
            with open(file_out, 'w') as f:
                print(text, file=f)

    return suffix_text_dict


if __name__ == '__main__':
    import sys

    print(sys.argv)

    # run CLI
    main()
