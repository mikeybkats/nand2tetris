import sys
# init: initializes the I/O files and drives the process


class FileHandler:
    def __init__(self, infile_path, outfile_path):
        """
        initializer - Opens the input file/stream and gets ready to parse it
        """
        self._infile_path = infile_path
        self._infile = self.open_input_file(infile_path)
        self._outfile = self.create_output_file(outfile_path)
        self._outfile_path = outfile_path

    def infile_path(self):
        return self._infile_path

    def infile(self):
        return self._infile

    def outfile(self):
        return self._outfile

    def outfile_path(self):
        return self._outfile_path

    def outfile_path(self, filename):
        self._outfile_path = filename

    def open_input_file(self, input_file):
        return open(input_file, mode='rt', encoding='utf-8')

    def create_output_file(self, infile_path):
        return open(infile_path, mode='w+', encoding='utf-8')

    def write_to_output_file(self, value):
        self._outfile.write(value)

    def print_output_file(self):
        output_file_contents = open(
            self._outfile_path, mode='rt', encoding='utf-8')
        for line in output_file_contents:
            sys.stdout.write(line)
