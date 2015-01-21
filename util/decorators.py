from functools import wraps


def each_filter(single, multi):
    """multi keyword is iterated and a function is applied, finally the results are collected"""
    def single_filter(f):
        @wraps(f)
        def _(*args, **kwargs):
            result = []
            lists = kwargs[multi]
            del kwargs[multi]
            for packets in lists:
                kwargs[single] = packets
                result.append(f(*args, **kwargs))
            return result
        return _
    return single_filter


packet_filter = each_filter('packets', 'packet_lists')
edge_operator = each_filter('edges', 'edge_lists')
graph_operator = each_filter('graph', 'graphs')