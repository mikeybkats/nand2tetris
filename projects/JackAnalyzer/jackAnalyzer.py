import sys
import os


class JackAnalyzer:
    def __init__(self):
        pass

    def parse_directory(self):
        # for each .jack file in the directory parse the file
        # and write the output to the output file
        pass

    def parse_file(self):
        # create a JackTokenizer from the xxx.jack input file
        pass

    def write_file_output(self):
        pass

    def create_output_file(self):
        # create an output file called xxx.xml
        pass


if __name__ == '__main__':
    infile_path = sys.argv[1]

    # if the infile_path is a directory
    # # parse all the files in the directory
    # else parse the single file
