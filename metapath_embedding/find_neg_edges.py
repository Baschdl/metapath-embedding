import argparse
from tqdm import tqdm
from neo4j.v1 import GraphDatabase
import os
from metapath_embedding.find_new_edges import NewEdgeFinder


def parse_arguments():
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('--folder_mined_metapaths',
                        help='Folder where the files with the mined meta-paths lie',
                        type=str,
                        required=True)
    parser.add_argument('--converted_new_edges_list',
                        help='Path to save converted "new edges" list',
                        type=str,
                        required=True)
    parser.add_argument('--neg_edges_list',
                        help='Path where to save the negative edges list',
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


def parse_ids_from_filename(filename: str):
    _, id1, id2 = (filename.split("-")[-1]).split("_")
    id2 = id2[:-4]
    return int(id1), int(id2)


if __name__ == "__main__":
    args = parse_arguments()
    neo = GraphDatabase.driver(args.uri, auth=(args.user, args.password))
    neg_edges = []
    new_edges = {}

    print("Loading new edges...")
    with open(args.converted_new_edges_list, 'r') as file:
        for line in tqdm(file):
            node1, node2 = NewEdgeFinder.split_edge(line)
            new_edges[(node1, node2)] = True

    print("Finding neg edges...")
    for file in tqdm(os.listdir(args.folder_mined_metapaths)):
        if "_converted.txt" in file:
            pass
        id1, id2 = parse_ids_from_filename(file)
        with neo.session() as session:
            result = session.run('MATCH (n1)--(n2) WHERE ID(n1) = {} AND ID(n2) = {} RETURN n1, n2'.format(id1, id2))
            result = [rec["n1, n2"] for rec in result]
            if not result and not new_edges.get((id1, id2), False):
                neg_edges.append((id1, id2))

    print("Writing to disk...")
    with open(args.neg_edges_list, 'w') as file:
        for node1, node2 in neg_edges:
            file.write("{} {}\n".format(node1, node2))
