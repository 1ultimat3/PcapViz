from util.decorators import packet_filter


def _expand(x):
    while x.payload:
        x = x.payload
        yield x.name

@packet_filter
def get_all_layers(packets):
    all_layers = set()
    for packet in packets:
        all_layers.update(list(_expand(packet)))
