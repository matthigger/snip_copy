from snip_copy.__main__ import parser, iter_file_out_value

from snip_copy.ipynb import snip_copy_ipynb, IPYNB


def main(args=None, write_new_file=True):
    """ loads a file, snip copies and optionally writes new file (ipynb)

    (this fnc allows us to test)
    Args:
        args: mimics sys.argv, defaults to actually using sys.argv
        write_new_file (bool): if True, writes new file

    Returns:
        stem_ipynb_dict (dict): keys are stem (str) of different outputs,
            values are str of text snipped per that stem
    """
    args = parser.parse_args(args=args)

    # read in file
    ipynb = IPYNB.from_file(f_ipynb=args.file_in)

    # snip and copy to make new files
    stem_ipynb_dict = snip_copy_ipynb(ipynb, regex_cmd=args.cmd)

    if write_new_file:
        for file_out, ipynb in iter_file_out_value(stem_ipynb_dict, args):
            ipynb.to_file(f_ipynb=file_out)

    return stem_ipynb_dict


if __name__ == '__main__':
    # run CLI
    main()
