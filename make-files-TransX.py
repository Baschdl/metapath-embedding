nodes_file_path = ""
nodes_out_file_path = ""

relations_file_path = ""
relations_out_file_path = ""

triplets_file_path = ""
triplets_out_file_path = ""


def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1


nodes = dict()
nodes_i = 0
count_nodes = file_len(nodes_file_path)
with open(nodes_file_path, "r") as nodes_file:
    with open(nodes_out_file_path, "r") as nodes_out_file:
        nodes_out_file.write("{}\n".format(count_nodes))
        for line in nodes_file:
            nodes[line] = nodes_i
            nodes_i += 1

relations_i = 0
relations = dict()
with open(nodes_out_file_path, "r") as relations_file:
    for line in relations_file:
        if line not in relations:
            relations[line] = relations_i
            relations_i += 1

relations2 = dict()
with open(relations_out_file_path, "r") as relations_out_file:
    relations_out_file.write("{}\n".format(relations_i))
    with open(relations_file_path, "r") as relations_file:
        for line in relations_file:
            if line not in relations2:
                relations2[line] = True
                relations_out_file.write("{} {}\n".format(line, relations[line]))


count_triplets = file_len(triplets_file_path)
with open(triplets_file_path, "r") as triplets_file:
    with open(triplets_out_file_path, "w") as triplets_out_file:
        triplets_out_file.write("{}\n".format(count_triplets))
        for line in triplets_file:
            #TODO: Which seperator?
            head, relation, tail = line.split("?")
            triplets_out_file.write("{} {} {}\n".format(nodes[head], relations[relation], nodes[tail]))