import os
from two_class_dict import TwoWayDict

infile_name = "MetaPaths-5-0.8_0_17414227.txt"
outfile_name = "MetaPaths-5-0.8_0_17414227_converted.txt"
filepath = "/Users/Sebastian/hpi/bachelorproject/metapath-embedding"


class Converter():
    d = TwoWayDict()

    @staticmethod
    def find_max_node_id(file_path: str):
        max_node_id = -1
        with open(os.path.join(filepath, infile_name), "r") as infile:
            for line in infile:
                line_separated = line[:-1].split("|")
                i = 0
                for char_number in line_separated:
                    if i % 2 == 0 and int(char_number) > max_node_id:
                        max_node_id = int(char_number)
                    i += 1
        return max_node_id

    def convert_file(self, infile_path: str, outfile_path: str, max_node_id: int):
        with open(infile_path, "r") as infile:
            with open(outfile_path, "w") as outfile:
                for line in infile:
                    line_separated = line[:-1].split("|")
                    line_utf = []
                    i = 0
                    for char_number in line_separated:
                        number = int(char_number)
                        if i % 2 == 0:
                            self.d[number] = chr(number)
                            line_utf.append(self.d[number])
                        else:
                            self.d[number + max_node_id] = chr(number + max_node_id)
                            line_utf.append(self.d[number + max_node_id])
                        i += 1
                    outfile.write("".join(line_utf) + "\n")

    def check_bijection(self, file_original: str, file_converted: str, max_node_id: int):
        with open(file_converted, "r") as infile_converted:
            with open(file_original, "r") as infile_original:
                for line_converted, line_original in zip(infile_converted, infile_original):
                    i = 0
                    for char_converted, char_original in zip(line_converted, line_original[:-1].split("|")):
                        if i % 2 == 0:
                            assert self.d[char_converted] == int(char_original), str(self.d[char_converted]) + "!=" + str(
                                char_original) + " for nodes"
                        else:
                            assert self.d[char_converted] - max_node_id == int(char_original), str(
                                self.d[char_converted + max_node_id]) + "!=" + str(char_original) + " for edges"
                        i += 1


if __name__ == "__main__":
    converter = Converter()
    max_node_id = converter.find_max_node_id(os.path.join(filepath, infile_name))
    print('Max_node_id is {}'.format(max_node_id))

    converter.convert_file(os.path.join(filepath, infile_name), os.path.join(filepath, outfile_name), max_node_id)

    print("Reversing...")
    converter.check_bijection(os.path.join(filepath, infile_name), os.path.join(filepath, outfile_name), max_node_id)

    print("Finished")
