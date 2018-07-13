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


if __name__ == "__main__":
    args = parse_arguments()
    neo = GraphDatabase.driver(args.uri, auth=(args.user, args.password))
    neo_ids = []
    with open(args.new_edges_list, 'r') as infile:
        with neo.session() as session:
            for line in tqdm(infile):
                node1, node2 = NewEdgeFinder.split_edge(line)
                result1 = session.run('MATCH (n) WHERE n.id = {} RETURN ID(n)'.format(node1))
                result2 = session.run('MATCH (n) WHERE n.id = {} RETURN ID(n)'.format(node2))
                neo_ids.append((result1, result2))

    with open(args.converted_new_edges_file, 'w') as file:
        for node1, node2 in neo_ids:
            file.write("{} {}\n".format(node1, node2))
