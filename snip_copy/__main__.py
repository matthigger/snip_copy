import argparse
import pathlib
from warnings import warn

from snip_copy.copy import snip_copy

description = 'creates copies of a file, snipping away portions of the ' \
              'original.  See https://github.com/matthigger/snip_copy'
parser = argparse.ArgumentParser(prog='snip_copy',
                                 description=description)
parser.add_argument('file_in', type=str, help='input file')
parser.add_argument('--cmd', type=str, default='# ?!',
                    help='regex to indicate start of command (e.g. '
                         '"snip-start" or "snip-end").  defaults to matching '
                         'on "#!" and "# !"')
parser.add_argument('--split', type=str, default=None,
                    help='if passed, gives copies of file, keeping all of '
                         'the file name before 1st occurrence of split.  the '
                         'remaining filename is given by stem argument. ('
                         'e.g. if your input file is `hw0_rub.py` you can '
                         'split on "_" to produce `hw0_sol.py` from command '
                         '`#! snip-start: sol`)')


def iter_file_out_value(stem_dict, args):
    """ iterates through stem, value pairs to compute file_out per value in dict

    - skips stem=None
        - this corresponds to the original text, with snip commands removed
    - gets file_out (utilizing split if need be)
    - checks file_out isn't the input file
        - warns and skips if so (don't want to overwrite this)

    Yields:
        file_out (pathlib.Path): output file
        value: value from original dict
    """
    # compute original file_in
    file_in = pathlib.Path(args.file_in)

    for stem, value in stem_dict.items():
        if stem is None:
            # stem is None has text of orig file with commands removed
            continue

        # build file_out
        if args.split is not None:
            # replace all text after final split with stem
            assert args.split in str(file_in.stem), \
                f'split char not in input file stem: {file_in}'
            stem_list = file_in.stem.split(args.split)
            stem_list[-1] = stem
            stem = args.split.join(stem_list)
        file_out = file_in.with_stem(stem)

        if file_in == file_out:
            # skip writing output (overwrites source file)
            warn(f'skipped: output file may not overwrite input ({file_in})')
            continue

        yield file_out, value


def main(args=None, write_new_file=True):
    """ loads a file, snip copies and optionally writes new file

    (this fnc allows us to test)
    Args:
        args: mimics sys.argv, defaults to actually using sys.argv
        write_new_file (bool): if True, writes new file

    Returns:
        stem_text_dict (dict): keys are stem (str) of different outputs,
            values are str of text snipped per that stem
    """
    args = parser.parse_args(args=args)

    # read in file
    with open(args.file_in) as f:
        text = f.read()

    # snip and copy to make new files
    stem_text_dict = snip_copy(text, regex_cmd=args.cmd)

    if write_new_file:
        for file_out, text in iter_file_out_value(stem_text_dict, args):
            # print text to output
            with open(file_out, 'w') as f:
                print(text, file=f)

    return stem_text_dict


if __name__ == '__main__':
    # run CLI
    main()
