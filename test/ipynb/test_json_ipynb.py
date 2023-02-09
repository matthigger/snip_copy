import pathlib

import snip_copy
from snip_copy.ipynb.json_ipynb import IPYNB

folder = pathlib.Path(snip_copy.__file__).parents[1] / 'test' / 'ex_hw'
f_ipynb = folder / 'simple.ipynb'


def test_ipynb():
    ipynb0 = IPYNB.from_file(f_ipynb=f_ipynb)
    ipynb1 = ipynb0.with_text(['a', 'b'])

    assert ipynb0 != ipynb1

    ipynb1.del_cell([1])
    assert ipynb1.text_list == ['a']
