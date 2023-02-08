from snip_copy.snip import *


def test_snipper():
    snip_list = [Snipper(1, 2), Snipper(3, 4)]

    assert str(snip_list[0]) == 'Snipper(idx_start=1, idx_stop=2)'
    assert snip_list[0] < snip_list[1]
    assert snip_list[0](range(6)) == [0, 2, 3, 4, 5]
    assert Snipper.apply_snip_list(snip_list, range(6)) == [0, 2, 4, 5]
