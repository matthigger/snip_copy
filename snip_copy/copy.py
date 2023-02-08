from collections import defaultdict

from .parse import parse_text, SNIP_START, SNIP_END
from .snip import Snipper


def snip_copy(text, **kwargs):
    """ returns copies of text with sections snipped out

    Args:
        text (str): text to operate on

    Returns:
        stem_text_dict (dict): keys are stem (str) of different outputs,
            values are str of text snipped per that stem
    """

    # extract commands
    line_list, cmd_list = parse_text(text, **kwargs)

    # build list of snip objects (per stem)
    stem_snip_list_dict = defaultdict(list)
    for idx in range(0, len(cmd_list), 2):
        cmd_snip_start = cmd_list[idx]
        assert cmd_snip_start.type == SNIP_START, f'non-alternating {SNIP_START} / {SNIP_END}'

        if idx + 1 < len(cmd_list):
            # another command exists in pair (should be snip end)
            assert cmd_list[idx + 1].type == SNIP_END
            idx_stop = cmd_list[idx + 1].line_idx
        else:
            # final snip command
            idx_stop = len(line_list)

        # build snipper, add to corresponding stem
        snipper = Snipper(idx_start=cmd_snip_start.line_idx,
                          idx_stop=idx_stop)
        for stem in cmd_snip_start.args:
            stem_snip_list_dict[stem].append(snipper)

    # apply snips (per stem)
    stem_text_dict = {None: '\n'.join(line_list)}
    for stem, snip_list in stem_snip_list_dict.items():
        _line_list = Snipper.apply_snip_list(snip_list, line_list)
        stem_text_dict[stem] = '\n'.join(_line_list)

    return stem_text_dict
