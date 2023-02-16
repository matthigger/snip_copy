from snip_copy.copy_file import snip_copy
from .json_ipynb import IPYNB


def snip_copy_ipynb(ipynb=None, file=None, **kwargs):
    """ returns copies of ipynb (json_dict) with sections snipped out

    Args:
        ipynb (IPYNB): input jupyter notebook
        file (str): path to an ipynb notebook

    Returns:
        stem_ipynb_dict (dict): keys are stems (str).  values ipynb objects
    """
    assert (ipynb is None) != (file is None), 'either ipynb xor file required'

    if ipynb is None:
        # load ipynb from file
        ipynb = IPYNB.from_file(f_ipynb=file)

    # contains a stem_text_dict corresponding to each cell
    stem_text_dict_list = [snip_copy(text, **kwargs) for text in ipynb.text_list]

    # collect all stems
    set_stem = set()
    for stem_text_dict in stem_text_dict_list:
        set_stem |= stem_text_dict.keys()

    # build ipynb per each stem
    stem_ipynb_dict = dict()
    for stem in set_stem:
        # text_list is a list of text, per each cell.  del_list holds idx of cells to deleted
        text_list = list()
        del_list = list()
        for cell_idx, stem_text_dict in enumerate(stem_text_dict_list):
            # stem_text is key in stem_dict_dict with proper text
            stem_text = stem
            if stem not in stem_text_dict:
                # stem not explicitly mentioned in cell, use given cell text
                # with any commands removed
                stem_text = None
            elif not stem_text_dict[stem]:
                # stem mentioned in cell & empty text is the result -> del cell
                del_list.append(cell_idx)
            text_list.append(stem_text_dict[stem_text])

        # build new ipynb per given text_list and del_list
        _ipynb = ipynb.with_text(text_list)
        _ipynb.del_cell(del_list)
        stem_ipynb_dict[stem] = _ipynb

    return stem_ipynb_dict
