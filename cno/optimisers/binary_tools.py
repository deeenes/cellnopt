import itertools



def permutations(L, M=1):
    """Create all the permutations of a bitstring of length L
    M : max value of the parameter. For instance to get all combination
    of 0,1 and 2 of strings of length 10 perm(10, 2)
    """
    a = itertools.product(range(0, M+1), repeat=L)
    return a # this is an iterator.

