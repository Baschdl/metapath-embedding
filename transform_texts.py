import os
from two_class_dict import TwoWayDict
import time
import argparse
from tqdm import tqdm


class Converter():
    d = TwoWayDict()

    @staticmethod
    def split_line(self, line):
        if line[-1] == '\n':
            return line[:-1].split("|")
        else:
            return line.split("|")

    @staticmethod
    def find_max_node_id(file_path: str):
        max_node_id = -1
        with open(file_path, "r") as infile:
            for line in infile:
                line_separated = Converter.split_line(line)
                i = 0
                for char_number in line_separated:
                    try:
                        number = int(char_number)
                    except ValueError as e:
                        print("Error for file {} in line '{}'".format(file_path, line))
                        print(e)
                    if i % 2 == 0 and number > max_node_id:
                        max_node_id = number
                    i += 1
        return max_node_id

    def convert_file(self, infile_path: str, outfile_path: str, max_node_id: int):
        with open(infile_path, "r") as infile:
            with open(outfile_path, "w") as outfile:
                for line in infile:
                    line_separated = Converter.split_line(line)
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
                            assert self.d[char_converted] == int(char_original), str(
                                self.d[char_converted]) + "!=" + str(
                                char_original) + " for nodes"
                        else:
                            assert self.d[char_converted] - max_node_id == int(char_original), str(
                                self.d[char_converted + max_node_id]) + "!=" + str(char_original) + " for edges"
                        i += 1


def parse_arguments():
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('--dirpath',
                        help='Path where meta-path files are located',
                        type=str,
                        required=True)

    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()

    converter = Converter()
    max_node_id = -1
    start = time.time()
    for file in tqdm(os.listdir(args.dirpath)):
        if not '_converted.txt' in file:
            file_max_node_id = converter.find_max_node_id(os.path.join(args.dirpath, file))
            if file_max_node_id > max_node_id:
                max_node_id = file_max_node_id
    end = time.time()
    print("Max node time: {}".format(end - start))
    print('Max_node_id is {}'.format(max_node_id))

    start = time.time()
    for file in tqdm(os.listdir(args.dirpath)):
        if not '_converted.txt' in file:
            converter.convert_file(os.path.join(args.dirpath, file),
                                   os.path.join(args.dirpath, file[:-4] + '_converted.txt'),
                                   max_node_id)
    end = time.time()
    print("Converting time is {}".format(end - start))

    print("Reversing...")
    start = time.time()
    for file in tqdm(os.listdir(args.dirpath)):
        if not '_converted.txt' in file:
            converter.check_bijection(os.path.join(args.dirpath, file),
                                      os.path.join(args.dirpath, file[:-4] + "_converted.txt"),
                                      max_node_id)
    end = time.time()
    print("Check bijection time is {}".format(end - start))

    print("Finished")
