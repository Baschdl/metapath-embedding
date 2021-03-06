import os
from metapath_embedding.two_class_dict import TwoWayDict
import time
import argparse
from multiprocessing import Pool
from typing import Tuple
import errno
import random


class Converter:
    def __init__(self):
        pass

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
    def convert_file(args: Tuple[str, str, str, str, int, int, int]):
        filename, infile_path, outfile_path, outfile_fasttext_path, max_node_id, sentence_length = args

        try:
            os.makedirs(outfile_path)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise
        try:
            os.makedirs(outfile_fasttext_path)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise

        infile_path = os.path.join(infile_path, filename)
        outfile_path = os.path.join(outfile_path, filename[:-4] + '_converted.txt')
        outfile_fasttext_path = os.path.join(outfile_fasttext_path, filename[:-4] + '_fasttext.txt')

        with open(infile_path, "r") as infile:
            with open(outfile_path, "wb") as outfile:
                lines_utf = []
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
                            line_utf.append(Converter.convert_node(number))
                        else:
                            line_utf.append(Converter.convert_edge(max_node_id, number))
                        i += 1
                    line_utf.append("\n")
                    outfile.write(u"".join(line_utf).encode('utf-8'))
                    if sentence_length != 0:
                        lines_utf.append(line_utf)
                if sentence_length != 0:
                    files = {}
                    for i in range(sentence_length):
                        files[i] = lines_utf.copy()
                        random.shuffle(files[i])
                    with open(outfile_fasttext_path, "w") as outfile_fasttext:
                        for j in range(len(files[0])):
                            sentence = []
                            for i in range(sentence_length):
                                sentence.append("".join(files[i][j]))
                            outfile_fasttext.write(" ".join(sentence) + "\n")

    @staticmethod
    def convert_edge(number, max_node_id):
        return chr(number + max_node_id)

    @staticmethod
    def convert_node(number):
        return chr(number)

    @staticmethod
    def reverse_edge(codepoint, max_node_id):
        return ord(codepoint) - max_node_id

    @staticmethod
    def reverse_node(codepoint):
        return ord(codepoint)


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
    parser.add_argument('--sentence_length',
                        help='Specify how long a sentence should be. 0 if no output files for fasttext should be produced.',
                        type=int,
                        required=True),
    parser.add_argument('--max_node_id',
                        help='Specify max_node_id obtained from another run of the program',
                        type=int)

    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()

    converter = Converter()

    pool = Pool(processes=args.processes)

    if args.max_node_id is None:
        start = time.time()
        print('Searching max_node_id...')
        files = [os.path.join(args.dirpath, file) for file in os.listdir(args.dirpath) if
                 os.path.isfile(os.path.join(args.dirpath, file)) and not '_converted.txt' in file]
        results = pool.map(Converter.find_max_node_id, files)
        max_node_id = -1
        for file_max_node_id in results:
            if file_max_node_id > max_node_id:
                max_node_id = file_max_node_id
        end = time.time()
        print("Max node time: {} seconds".format(end - start))
        print('Max_node_id is {}'.format(max_node_id))
    else:
        max_node_id = args.max_node_id

    print("Start conversion of files...")
    start = time.time()
    args = [(file,
             args.dirpath,
             os.path.join(args.dirpath, 'converted'),
             os.path.join(args.dirpath, 'fasttext'),
             max_node_id,
             args.sentence_length)
            for file in os.listdir(args.dirpath) if
            os.path.isfile(os.path.join(args.dirpath, file)) and
            '_converted.txt' not in file or
            os.path.exists(os.path.join(args.dirpath, file[:-4] + '_converted.txt')) or
            os.path.exists(os.path.join(args.dirpath, 'converted', file[:-4] + '_converted.txt'))]

    pool.map(Converter.convert_file, args)

    end = time.time()
    print("Converting time is {}".format(end - start))

    print("Finished")
