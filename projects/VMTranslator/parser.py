import sys


class Parser:
    def __init__(self, infile_path, outfile_path):
        self._infile_path = infile_path
        self._outfile_path = outfile_path

        print("starting parser", self._infile_path, self._outfile_path)

    def infile(self):
        return self._infile_path

    def outfile(self):
        return self._outfile_path


if __name__ == '__main__':
    outfile_path = 'output.asm'
    if len(sys.argv) == 3:
        outfile_path = sys.argv[2]

    Parser(infile_path=sys.argv[1], outfile_path=outfile_path)
