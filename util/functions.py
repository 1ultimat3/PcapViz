from itertools import chain

def combine_lists(lists):
    return [list(chain(*lists))]