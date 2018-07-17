import argparse
from tqdm import tqdm
from find_new_edges import NewEdgeFinder
from neo4j.v1 import GraphDatabase


def parse_arguments():
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('--new_edges_list',
                        help='Path to "new edges" list',
                        type=str,
                        required=True)
    parser.add_argument('--converted_new_edges_list',
                        help='Path to save converted "new edges" list',
                        type=str,
                        required=True)
    parser.add_argument('--uri',
                        help='Bolt address of neo4j instance',
                        type=str,
                        required=True)
    parser.add_argument('--user',
                        help='User name of neo4j instance',
                        type=str,
                        required=True)
    parser.add_argument('--password',
                        help='Password of neo4j instance',
                        type=str,
                        required=True)

    return parser.parse_args()


def clean_qids(node):
    if node[0] == "'" and node[-1] == "'":
        return (node[1:])[:-1]
    else:
        return node


if __name__ == "__main__":
    args = parse_arguments()
    neo = GraphDatabase.driver(args.uri, auth=(args.user, args.password))
    neo_ids = []
    edges_with_new_nodes = 0
    with open(args.new_edges_list, 'r') as infile:
        with neo.session() as session:
            for line in tqdm(infile):
                node1, node2 = NewEdgeFinder.split_edge(line)
                node1 = clean_qids(node1)
                node2 = clean_qids(node2)
                result1 = session.run('MATCH (n:Item) WHERE n.id = "{}" RETURN ID(n)'.format(node1))
                result1 = [rec["ID(n)"] for rec in result1]
                if not result1:
                    edges_with_new_nodes += 1
                    continue
                id_node1 = result1[0]
                result2 = session.run('MATCH (n:Item) WHERE n.id = "{}" RETURN ID(n)'.format(node2))
                result2 = [rec["ID(n)"] for rec in result2]
                if not result2:
                    edges_with_new_nodes += 1
                    continue
                id_node2 = result2[0]
                neo_ids.append((id_node1, id_node2))
    print("There were {} eges with new nodes".format(edges_with_new_nodes))

    with open(args.converted_new_edges_list, 'w') as file:
        for node1, node2 in neo_ids:
            file.write("{} {}\n".format(node1, node2))
