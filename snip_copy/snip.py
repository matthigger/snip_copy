class Snipper:
    """ removes a contiguous run of items from a list

    Attributes:
        idx_start (idx): index to start removing items
        idx_stop (idx): index to stop removing items (item with this index
            remains in the list, like a python slice)
    """

    def __init__(self, idx_start, idx_stop):
        self.idx_start = idx_start
        self.idx_stop = idx_stop
        assert idx_stop > idx_start

    def __repr__(self):
        return 'Snipper(idx_start={idx_start}, idx_stop={idx_stop})'.format(**self.__dict__)

    def __lt__(self, other):
        """ determines if one snip target occurs before another """
        assert isinstance(other, Snipper)
        assert self.idx_stop < other.idx_start or \
               other.idx_stop < self.idx_start, 'overlapping snip targets'

        return self.idx_stop < other.idx_start

    def __call__(self, x):
        """ applies snip operation to a list

        Args:
            x (list): a list
        """
        x = list(x)
        return x[:self.idx_start] + x[self.idx_stop:]

    @classmethod
    def apply_snip_list(cls, snip_list, x):
        """ applies many snip operations (assumed non overlapping)

        Args:
            snip_list (list): a list of snip_target objects
            x (list): input list

        Returns:
            x_snipped (list): list with lines snipped out
        """
        for snipper in sorted(snip_list, reverse=True):
            x = snipper(x)

        return x
