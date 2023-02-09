import json
from copy import deepcopy


class IPYNB:
    """ loads, saves and compares ipynb json files

    jupyter's json format has cell id's which change with every run.
    additionally, text is stored as a list of strings, broken at every new
    line (but somehow still including newline chars?).  jupyter still loads
    an ipynb which stores each cell's source as a full string.

    it is more convenient, for our purposes, to just deal with a list of
    strings representing the contents of every cell.  this object largely hides
    the actual json_dict from use.

    Attributes:
        json_dict (dict): json dict, loaded from source
        text_list (list): a list of strings, the text of corresponding cells
    """

    def to_file(self, f_ipynb):
        with open(f_ipynb, 'w') as f:
            json.dump(self.json_dict, f)

    @classmethod
    def from_file(cls, f_ipynb):
        with open(f_ipynb) as f:
            json_dict = json.load(f)

        text_list = [''.join(d['source']) for d in json_dict['cells']]

        return IPYNB(json_dict=json_dict, text_list=text_list)

    def __init__(self, json_dict, text_list):
        self.json_dict = json_dict
        self.text_list = text_list

    def __eq__(self, other):
        return self.text_list == other.text_list

    def del_cell(self, del_list):
        """ deletes cells from ipynb

        Args:
            del_list (list): a list of cell idx to delete
        """
        for cell_idx in sorted(del_list, reverse=True):
            del self.json_dict['cells'][cell_idx]
            self.text_list.pop(cell_idx)

    def with_text(self, text_list):
        """ creates new ipynb object with given text_list

        Args:
            text_list (list): a list of text of every cell in ipynb

        Returns:
            ipynb (IPYNB): new ipynb, with text replaced
        """

        n = len(self.json_dict['cells'])
        assert len(text_list) == n, \
            f'input has {len(text_list)} cells while ipynb has {n} cells'

        # build copy of json dict to text_list & del_list spec above
        json_dict = deepcopy(self.json_dict)

        # update each cell with given text
        for cell_idx, text in enumerate(text_list):
            json_dict['cells'][cell_idx]['source'] = text

        return IPYNB(json_dict=json_dict, text_list=text_list)
