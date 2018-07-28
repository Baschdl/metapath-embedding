import random
import argparse
from multiprocessing.pool import Pool

import os
from tqdm import tqdm

from metapath_embedding.find_new_edges import NewEdgeFinder


def filter(all_edges_filepath, filtered_edges_filepath, part_of_nodes, number_of_subsamples):
    print("Read all nodes and edges...")
    edges = []
    nodes = set()
    with open(all_edges_filepath, 'r') as all_edges_file:
        for line in tqdm(all_edges_file):
            node0, node1 = NewEdgeFinder.split_edge(line)
            node0, node1 = int(node0), int(node1)
            edges.append((node0, node1))
            nodes.add(node0)
            nodes.add(node1)

    print("Sample nodes...")
    nodes_subsamples = []
    for i in range(number_of_subsamples):
        nodes_subsamples.append(random.sample(nodes, int(part_of_nodes * len(nodes))))
    print("Write new edges to file...")
    args = []
    for subsample in nodes_subsamples:
        args.append((edges, filtered_edges_filepath, subsample))
    pool = Pool()
    pool.map(write_edgelist_to_file, args)


def write_edgelist_to_file(args):
    edges, filtered_edges_filepath, nodes_subsample = args
    filtered_edges = []
    args = []
    for nodes_subsample_part in chunkIt(nodes_subsample, os.cpu_count()):
        args.append((edges, filtered_edges, nodes_subsample_part))
    pool = Pool()
    results = pool.map(filter_edges, args)
    for result in results:
        filtered_edges.extend(result)
    with open(filtered_edges_filepath, 'w') as all_edges_file:
        for edge in filtered_edges:
            all_edges_file.write("{} {}\n".format(edge[0], edge[1]))


def filter_edges(args):
    edges, filtered_edges, nodes_subsample = args
    for edge in tqdm(edges):
        if edge[0] in nodes_subsample and edge[1] in nodes_subsample:
            filtered_edges.append(edge)


def chunkIt(seq, num):
    # Code from https://stackoverflow.com/a/2130035/3342058
    avg = len(seq) / float(num)
    out = []
    last = 0.0

    while last < len(seq):
        out.append(seq[int(last):int(last + avg)])
        last += avg

    return out


def parse_arguments():
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('--all_edges_filepath',
                        type=str,
                        required=True)
    parser.add_argument('--filtered_edges_filepath',
                        type=str,
                        required=True)
    parser.add_argument('--part_of_nodes',
                        type=float,
                        required=True)
    parser.add_argument('--number_of_subsamples',
                        type=int,
                        required=True)

    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()
    filter(args.all_edges_filepath, args.filtered_edges_filepath, args.part_of_nodes, number_of_subsamples)
