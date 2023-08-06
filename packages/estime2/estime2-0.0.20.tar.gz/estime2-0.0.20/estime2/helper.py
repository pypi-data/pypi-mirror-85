
def diff(one, other):
    '''
    Return element(s) of `one` that is/are not an element of `other`.

    Usage
    -----
    `difference(one, other)`

    Examples
    --------
    >>> one = ['a', 'b']
    >>> other = ['a', 'c']
    >>> is_subset(one, other)
    False
    >>> diff(one, other)
    ['b']
    '''

    if not isinstance(one, set):
        one = set(one)
    if not isinstance(other, set):
        other = set(other)

    return list(one.difference(other))

def is_subset(one, other):
    '''
    Return True if `one` is the subset of the `other`.

    Usage
    -----
    `is_subset(one, other)`

    Examples
    --------
    >>> one = ['a']
    >>> other = ['a', 'b']
    >>> is_subset(one, other)
    True
    '''

    if not isinstance(one, set):
        one = set(one)
    if not isinstance(other, set):
        other = set(other)
    
    return one.issubset(other)

def raise_if_not_subset(
    one, other, one_name = "one", other_name = "other"
):
    '''
    Raise AssertionError if `one` is not the subset of the `other`, and
    display item(s) of `one` that is/are not an element of `other`. Provide
    names of `one` and `other` to `one_name` and `other_name` if one wishes
    to see the argument names displayed in the error message. By default,
    they are "one" and "other" respectively.

    Usage
    -----
    `raise_if_not_subset(one, other, one_name, other_name)`
    '''

    msg =\
        '"{0}" is not a subset of "{1}" since the following item(s) ' +\
        'of "{0}" does/do not exist in "{1}": {2}'
    msg = msg.format(one_name, other_name, diff(one, other))
    assert is_subset(one, other), msg

def return_op_if_None(op, argument):
    '''
    Return `op` if `argument` is None. Otherwise, return `argument`.

    Usage
    -----
    `return_op_if_None(op, argument)`
    '''

    return op if argument is None else argument



if __name__ == '__main__':
    import doctest
    doctest.testmod()
