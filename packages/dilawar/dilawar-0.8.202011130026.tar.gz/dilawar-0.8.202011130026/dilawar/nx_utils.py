__author__           = "Dilawar Singh"
__copyright__        = "Copyright 2019-, Dilawar Singh"
__maintainer__       = "Dilawar Singh"
__email__            = "dilawars@ncbs.res.in"


def read_dot(dotfile):
    import networkx as nx
    try:
        return nx.drawing.nx_adot.read_dot(dotfile)
    except Exception as e:
        return nx.drawing.nx_pydot.read_dot(dotfile)

def test():
    import tempfile
    import io
    dot = io.StringIO('''
digraph D {
    a -> b;
    b -> c;
    } ''')
    g = read_dot(dot)
    assert g.number_of_nodes() == 3
    assert g.number_of_edges() == 2

def main():
    test()

if __name__ == '__main__':
    main()
