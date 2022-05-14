import sys
import os
from tokenizer import JackTokenizer


class CompilationEngine:
    def __init__(self):
        pass


if __name__ == '__main__':
    infile_path = sys.argv[1]

    tokenizer = JackTokenizer(infile_path)
