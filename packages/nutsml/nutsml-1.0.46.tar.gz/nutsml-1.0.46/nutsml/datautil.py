"""
.. module:: datautil
   :synopsis: Utility functions for non-image data
"""

import random as rnd
import collections as cl

from six import iteritems
from nutsflow.common import as_set


def isnan(x):
    """
    Check if something is NaN.

    >>> import numpy as np
    >>> isnan(np.NaN)
    True

    >>> isnan(0)
    False

    :param object x: Any object
    :return: True if x is NaN
    :rtype: bool
    """
    return x != x


def istensor(x, attrs=['shape', 'dtype', 'min', 'max']):
    """
    Return true if x has shape, dtype, min and max.

    Will be true for Numpy and PyTorch tensors.

    >>> import numpy as np
    >>> M = np.zeros((2,3))
    >>> istensor(M)
    True

    >>> istensor([1,2,3])
    False

    :param object x: Any object
    :param list[str] attrs: Object attributes that 'define' a tensor.
    :return: True if x is some tensor object.
    """
    return all(hasattr(x, a) for a in attrs)


def shapestr(array, with_dtype=False):
    """
    Return string representation of array shape.

    >>> import numpy as np
    >>> a = np.zeros((3,4))
    >>> shapestr(a)
    '3x4'

    >>> a = np.zeros((3,4), dtype='uint8')
    >>> shapestr(a, True)
    '3x4:uint8'

    :param ndarray array: Numpy array
    :param bool with_dtype: Append dtype of array to shape string
    :return: Shape as string, e.g shape (3,4) becomes 3x4
    :rtype: str
    """
    sstr = 'x'.join(str(int(d)) for d in array.shape)
    if with_dtype:
        sstr += ':' + str(array.dtype)
    return sstr


def stype(obj):
    """
    Return string representation of structured objects.

    >>> import numpy as np
    >>> a = np.zeros((3,4), dtype='uint8')
    >>> b = np.zeros((1,2), dtype='float32')

    >>> stype(a)
    '<ndarray> 3x4:uint8'

    >>> stype(b)
    '<ndarray> 1x2:float32'

    >>> stype([a, (b, b)])
    '[<ndarray> 3x4:uint8, (<ndarray> 1x2:float32, <ndarray> 1x2:float32)]'

    >>> stype([1, 2.0, [a], [b]])
    '[<int> 1, <float> 2.0, [<ndarray> 3x4:uint8], [<ndarray> 1x2:float32]]'

    >>> stype({'a':a, 'b':b, 'c':True})
    '{a:<ndarray> 3x4:uint8, b:<ndarray> 1x2:float32, c:<bool> True}'

    >>> from collections import namedtuple
    >>> Sample = namedtuple('Sample', 'x,y')
    >>> sample = Sample(a, 1)
    >>> stype(sample)
    'Sample(x=<ndarray> 3x4:uint8, y=<int> 1)'

    :param object obj: Any object
    :return: String representation of object where arrays are replace by their
             shape and dtype descriptions
    :rtype: str
    """
    typename = lambda obj: type(obj).__name__
    typestr = lambda obj: '<' + typename(obj) + '> '
    expr = lambda kv, s: str(kv[0]) + s + stype(kv[1])
    mklist = lambda obj: ', '.join(stype(o) for o in obj)
    mkset = lambda obj: ', '.join(stype(o) for o in sorted(obj))
    mkdict = lambda obj: ', '.join(expr(kv, ':') for kv in sorted(obj.items()))
    mkfields = lambda obj: ', '.join(expr(kv, '=') for kv in zip(obj._fields, obj))

    if istensor(obj, ['shape', 'dtype']):
        return typestr(obj) + shapestr(obj, True)
    if isinstance(obj, list):
        return '[' + mklist(obj) + ']'
    if isinstance(obj, tuple):
        if hasattr(obj, '_fields'):  # namedtuple
            return typename(obj) + '(' + mkfields(obj) + ')'
        return '(' + mklist(obj) + ')'
    if isinstance(obj, set):
        return '{' + mkset(obj) + '}'
    if isinstance(obj, dict):
        return '{' + mkdict(obj) + '}'

    return typestr(obj) + str(obj)


def batchstr(batch, with_dtype=True):
    """
    Return string representation of a batch/list of arrays.

    See shapestr(array) for details of array representation.

    >>> import numpy as np
    >>> a = np.zeros((3,4), dtype='uint8')
    >>> b = np.zeros((1,2,2), dtype='float16')
    >>> batchstr([a, b])
    '[3x4:uint8, 1x2x2:float16]'

    :param list batch: Iterable over numpy arrays
    :param bool with_dtype: Append dtype of array to shape string
    :return: String representation of the batch
    :rtype: str
    """
    return '[' + ', '.join(shapestr(b, with_dtype) for b in batch) + ']'


def upsample(samples, labelcol, rand=None):
    """
    Up-sample sample set.

    Creates stratified samples by up-sampling smaller classes to the size of
    the largest class.

    Note: The example shown below uses rnd.Random(i) to create a deterministic
    sequence of randomly stratified samples. Usually it is sufficient to use
    the default (rand=None).

    >>> from __future__ import print_function
    >>> import random as rnd
    >>> samples = [('pos1', 1), ('pos2', 1), ('neg1', 0)]
    >>> for i in range(3):  # doctest: +SKIP
    ...     print(upsample(samples, 1, rand=rnd.Random(i)))
    [('neg1', 0), ('neg1', 0), ('pos1', 1), ('pos2', 1)]
    [('pos2', 1), ('neg1', 0), ('pos1', 1), ('neg1', 0)]
    [('neg1', 0), ('neg1', 0), ('pos1', 1), ('pos2', 1)]

    :param iterable samples: Iterable of samples where each sample has a
      label at a fixed position (labelcol). Labels can by any hashable type,
      e.g. int, str, bool
    :param int labelcol: Index of label in sample
    :param Random|None rand: Random number generator. If None,
           random.Random(None) is used.
    :return: Stratified sample set.
    :rtype: list of samples
    """

    rand = rnd.Random() if rand is None else rand
    groups, labelcnts = group_samples(samples, labelcol)
    _, max_cnts = max(iteritems(labelcnts), key=lambda l_c: l_c[1])
    stratified = []
    for label, samples in iteritems(groups):
        extended = samples * int((max_cnts / len(samples) + 1))
        stratified.extend(extended[:max_cnts])
    rand.shuffle(stratified)
    return stratified


def random_downsample(samples, labelcol, rand=None, ordered=False):
    """
    Randomly down-sample samples.

    Creates stratified samples by down-sampling larger classes to the size of
    the smallest class.

    Note: The example shown below uses StableRandom(i) to create a deterministic
    sequence of randomly stratified samples. Usually it is sufficient to use
    the default (rand=None). Do NOT use rnd.Random(0) since this
    will generate the same subsample every time.

    >>> from __future__ import print_function  
    >>> from nutsflow.common import StableRandom

    >>> samples = [('pos1', 1), ('pos2', 1), ('pos3', 1),
    ...            ('neg1', 0), ('neg2', 0)]
    >>> for i in range(3):
    ...     print(random_downsample(samples, 1, StableRandom(i), True))
    [('pos2', 1), ('pos3', 1), ('neg2', 0), ('neg1', 0)]
    [('pos2', 1), ('pos3', 1), ('neg2', 0), ('neg1', 0)]
    [('pos2', 1), ('pos1', 1), ('neg1', 0), ('neg2', 0)]

    :param iterable samples: Iterable of samples where each sample has a
      label at a fixed position (labelcol). Labels can be any hashable type,
      e.g. int, str, bool
    :param int labelcol: Index of label in sample
    :param Random|None rand: Random number generator. If None,
      random.Random(None) is used.
    :param bool ordered: True: samples are kept in order when downsampling.
    :return: Stratified sample set.
    :rtype: list of samples
    """
    rand = rnd.Random() if rand is None else rand
    groups, labelcnts = group_samples(samples, labelcol, ordered=ordered)
    _, min_cnts = min(iteritems(labelcnts), key=lambda l_c1: l_c1[1])
    return [s for e in groups.values() for s in rand.sample(e, min_cnts)]


def group_samples(samples, labelcol, ordered=False):
    """
    Return samples grouped by label and label counts.

    >>> samples = [('pos', 1), ('pos', 1), ('neg', 0)]  
    >>> groups, labelcnts = group_samples(samples, 1, True)
    >>> groups
    OrderedDict([(1, [('pos', 1), ('pos', 1)]), (0, [('neg', 0)])])

    >>> labelcnts
    Counter({1: 2, 0: 1})

    :param iterable samples: Iterable of samples where each sample has a
      label at a fixed position (labelcol)
    :param int labelcol: Index of label in sample
    :param bool ordered: True: samples are kept in order when grouping.
    :return: (groups, labelcnts) where groups is a dict containing
      samples grouped by label, and labelcnts is a Counter dict
      containing label frequencies.
    :rtype: tuple(dict, Counter)
    """
    labelcnts = cl.Counter(s[labelcol] for s in samples)
    groups = group_by(samples, lambda s: s[labelcol], ordered=ordered)
    return groups, labelcnts


def group_by(elements, keyfunc, ordered=False):
    """
    Group elements using the given key function.

    >>> is_odd = lambda x: bool(x % 2)
    >>> numbers = [0, 1, 2, 3, 4]
    >>> group_by(numbers, is_odd, True)
    OrderedDict([(False, [0, 2, 4]), (True, [1, 3])])

    :param iterable elements: Any iterable
    :param function keyfunc: Function that returns key to group by
    :param bool ordered: True: return OrderedDict else return dict
    :return: dictionary with results of keyfunc as keys and the elements
             for that key as value
    :rtype: dict|OrderedDict
    """
    groups = cl.OrderedDict() if ordered else dict()
    for e in elements:
        key = keyfunc(e)
        if key in groups:
            groups[key].append(e)
        else:
            groups[key] = [e]
    return groups


def col_map(sample, columns, func, *args, **kwargs):
    """
    Map function to given columns of sample and keep other columns

    >>> sample = (1, 2, 3)
    >>> add_n = lambda x, n: x + n
    >>> col_map(sample, 1, add_n, 10)
    (1, 12, 3)

    >>> col_map(sample, (0, 2), add_n, 10)
    (11, 2, 13)

    :param tuple|list sample: Sample
    :param int|tuple columns: Single or multiple column indices.
    :param function func: Function to map
    :param args args: Arguments passed on to function
    :param kwargs kwargs: Keyword arguments passed on to function
    :return: Sample where function has been applied to elements in the given
            columns.
    """
    colset = as_set(columns)
    f, a, kw = func, args, kwargs
    enum_iter = enumerate(sample)
    return tuple(f(e, *a, **kw) if i in colset else e for i, e in enum_iter)


def shuffle_sublists(sublists, rand):
    """
    Shuffles the lists within a list but not the list itself.

    >>> from nutsflow.common import StableRandom
    >>> rand = StableRandom(0)

    >>> sublists = [[1, 2, 3], [4, 5, 6, 7]]
    >>> shuffle_sublists(sublists, rand)
    >>> sublists
    [[1, 3, 2], [4, 5, 7, 6]]

    :param sublists: A list containing lists
    :param Random rand: A random number generator.
    """
    for sublist in sublists:
        rand.shuffle(sublist)
