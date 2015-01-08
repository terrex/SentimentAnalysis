__author__ = 'terrex'

from collections import namedtuple


__all__ = ['Sample']

Sample = namedtuple('Sample', ['words', 'category'])
