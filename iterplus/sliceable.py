# -*- coding: utf-8 -*-
from itertools import islice

class sliceable(object):

    def __init__(self, it):
        self._iter = iter(it)
        self._cache = []

    def __getitem__(self, k):
        if isinstance(k, slice):
            return list(islice(self, k.start, k.stop, k.step))

        try:
            return next(islice(self, k, k+1))
        except StopIteration:
            raise IndexError('index out of range')

    def __iter__(self):
        for entry in self._cache:
            yield entry

        for entry in self._iter:
            self._cache.append(entry)
            yield entry

    def next(self):
        return next(iter(self))


if __name__ == '__main__':
    s = sliceable(xrange(4))
    assert s[:] == [0, 1, 2, 3]
    assert s[:1] == [0]
    assert s[1:] == [1, 2, 3]
    assert s[:10] == [0, 1, 2, 3]
    assert s[0:1] == [0]
    assert s[1] == 1
    assert list(s) == [0, 1, 2, 3]

    try:
        s[5]
    except IndexError:
        pass
    else:
        assert False
