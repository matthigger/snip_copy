import pathlib

import snip_copy
from snip_copy.ipynb.copy import snip_copy_ipynb
from snip_copy.ipynb.json_ipynb import IPYNB

folder = pathlib.Path(snip_copy.__file__).parents[1] / 'test' / 'ex_hw'
stem_ipynb_dict = dict()
for f_ipynb in folder.glob('*.ipynb'):
    stem_ipynb_dict[f_ipynb.stem] = IPYNB.from_file(f_ipynb=f_ipynb)


def test_snip_copy_ipynb():
    stem_json_dict = snip_copy_ipynb(ipynb=stem_ipynb_dict['rubric'])

    assert stem_ipynb_dict['solution'] == stem_json_dict['solution']
    assert stem_ipynb_dict['student'] == stem_json_dict['student']
