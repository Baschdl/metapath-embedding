import os
from two_class_dict import TwoWayDict
import time
import argparse
from tqdm import tqdm
from multiprocessing import Pool


class Converter():
    d = TwoWayDict()

    @staticmethod
    def split_line(line):
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

    @staticmethod
    def convert_file(infile_path: str, outfile_path: str, max_node_id: int):
        with open(infile_path, "r") as infile:
            with open(outfile_path, "w") as outfile:
                for line in infile:
                    line_separated = Converter.split_line(line)
                    line_utf = []
                    i = 0
                    for number_as_char in line_separated:
                        try:
                            number = int(number_as_char)
                        except ValueError as e:
                            print("Error for file {} in line '{}'".format(infile_path, line))
                            print(e)
                        if i % 2 == 0:
                            line_utf.append(chr(number))
                        else:
                            line_utf.append(chr(number + max_node_id))
                        i += 1
                    outfile.write("".join(line_utf) + "\n")


def parse_arguments():
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('--dirpath',
                        help='Path where meta-path files are located',
                        type=str,
                        required=True)
    parser.add_argument('--processes',
                        help='Specify number of processes which should be used for the conversion',
                        type=int,
                        required=True)

    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()

    converter = Converter()
    start = time.time()

    pool = Pool(processes=args.processes)
    files = [os.path.join(args.dirpath, file) for file in os.listdir(args.dirpath) if not '_converted.txt' in file]
    results = []
    for x in tqdm.tqdm(pool.map(Converter.find_max_node_id, files), total=len(files)):
        results.append(x)
    max_node_id = -1
    for file_max_node_id in results:
        if file_max_node_id > max_node_id:
            max_node_id = file_max_node_id
    end = time.time()
    print("Max node time: {}".format(end - start))
    print('Max_node_id is {}'.format(max_node_id))

    start = time.time()
    args = [(os.path.join(args.dirpath, file),
             os.path.join(args.dirpath, file[:-4] + '_converted.txt'),
             max_node_id)
            for file in os.listdir(args.dirpath) if
            not '_converted.txt' in file or os.path.exists(file[:-4] + '_converted.txt')]

    for _ in tqdm.tqdm(pool.map(Converter.convert_file, args), total=len(args)):
        pass

    end = time.time()
    print("Converting time is {}".format(end - start))

    print("Finished")
