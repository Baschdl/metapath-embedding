import os

class TwoWayDict(dict):
    def __setitem__(self, key, value):
        # Remove any previous connections with these values
        if key in self:
            assert self[key] == value, str(self[key]) + "!=" + str(value)
        if value in self:
            assert self[value] == key, str(self[value]) + "!=" + str(key)
        dict.__setitem__(self, key, value)
        dict.__setitem__(self, value, key)

    def __delitem__(self, key):
        dict.__delitem__(self, self[key])
        dict.__delitem__(self, key)

    def __len__(self):
        """Returns the number of connections"""
        return dict.__len__(self) // 2

infile_name = "MetaPaths-5-0.8_0_17414227.txt"
outfile_name = "MetaPaths-5-0.8_0_17414227_converted.txt"
filepath = "/Users/Sebastian/hpi/bachelorproject/metapath-embedding"

d = TwoWayDict()
max_node_id = -1

with open(os.path.join(filepath, infile_name), "r") as infile:
    for line in infile:
        line_separated = line[:-1].split("|")
        i = 0
        for char_number in line_separated:
            if i % 2 == 0 and int(char_number) > max_node_id:
                max_node_id = int(char_number)
            i += 1

print('Max_node_id is {}'.format(max_node_id))

with open(os.path.join(filepath, infile_name), "r") as infile:
    with open(os.path.join(filepath, outfile_name), "w") as outfile:
        for line in infile:
            line_separated = line[:-1].split("|")
            line_utf = []
            i = 0
            for char_number in line_separated:
                number = int(char_number)
                if i % 2 == 0:
                    d[number] = chr(number)
                    line_utf.append(d[number])
                else:
                    d[number + max_node_id] = chr(number + max_node_id)
                    line_utf.append(d[number + max_node_id])
                i += 1
            outfile.write("".join(line_utf) + "\n")

print("Reversing...")

with open(os.path.join(filepath, outfile_name), "r") as infile_converted:
    with open(os.path.join(filepath, infile_name), "r") as infile_original:
        for line_converted, line_original in zip(infile_converted,infile_original):
            i = 0
            for char_converted, char_original in zip(line_converted,line_original[:-1].split("|")):
                if i % 2 == 0:
                    assert d[char_converted] == int(char_original), str(d[char_converted]) + "!=" + str(char_original) + " for nodes"
                else:
                    assert d[char_converted]-max_node_id == int(char_original), str(d[char_converted +max_node_id]) + "!=" + str(char_original) + " for edges"
                i += 1
