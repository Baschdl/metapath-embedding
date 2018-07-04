import argparse


class NewEdgeFinder():
    edges_earlier_db = {}

    def __init__(self, earlier_edge_list_filepath, later_edge_list_filepath, directed=True):
        self.earlier_edge_list_filepath = earlier_edge_list_filepath
        self.later_edge_list_filepath = later_edge_list_filepath
        self.directed = directed

    def find(self):
        self._fill_dictionary()
        return self._find_new_edges()

    def _fill_dictionary(self):
        for edge in open(self.earlier_edge_list_filepath, 'r'):
            node1, node2 = self.split_edge(edge)
            if self.directed:
                self.edges_earlier_db[(node1, node2)] = True
            else:
                if (node1, node2) in self.edges_earlier_db:
                    continue
                elif (node2, node1) in self.edges_earlier_db:
                    continue
                else:
                    self.edges_earlier_db[(node1, node2)] = True

    def _find_new_edges(self):
        new_edges = {}
        for edge in open(self.later_edge_list_filepath, 'r'):
            node1, node2 = self.split_edge(edge)
            if not (node1, node2) in self.edges_earlier_db:
                if self.directed:
                    new_edges[(node1, node2)] = True
                else:
                    if not (node2, node1) in self.edges_earlier_db and not (node2, node1) in new_edges:
                        new_edges[(node1, node2)] = True
        return list(new_edges.keys())

    def split_edge(self, edge):
        if edge[-1] == '\n':
            return edge[:-1].split(" ")
        else:
            return edge.split(" ")


def parse_arguments():
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('--earlier_edge_list',
                        help='Path to earlier edge list',
                        type=str,
                        required=True)
    parser.add_argument('--later_edge_list',
                        help='Path to later edge list',
                        type=str,
                        required=True)
    parser.add_argument('--directed',
                        help='Treat graph as directed',
                        type=bool,
                        default=True)

    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()
    new_edges = NewEdgeFinder(args.earlier_edge_list, args.later_edge_list, args.directed).find()
    print(new_edges)
