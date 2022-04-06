import sys
import os


class FileHandler:
    def __init__(self, infile_path, outfile_path):
        """
        initializer - Opens the input file/stream and gets ready to parse it
        """
        self._infile_path = infile_path
        self._outfile_path = outfile_path
        self._outfile = self.create_output_file(outfile_path, "w+")
        self._infile = None

        if os.path.isdir(infile_path):
            self._outfile.close()
            self._outfile = self.create_output_file(outfile_path, "a")

    @property
    def infile_path(self):
        return self._infile_path

    @infile_path.setter
    def infile_path(self, new_path):
        self._infile_path = new_path

    @property
    def infile(self):
        return self._infile

    @property
    def outfile(self):
        return self._outfile

    @outfile.setter
    def outfile(self, new_outfile):
        self._outfile = new_outfile

    @property
    def outfile_path(self):
        return self._outfile_path

    @outfile_path.setter
    def outfile_path(self, filename):
        self._outfile_path = filename

    def open_input_file(self):
        self._infile = open(self._infile_path, mode='rt', encoding='utf-8')

    def create_output_file(self, infile_path, mode):
        return open(infile_path, mode=mode, encoding='utf-8')

    def write_to_output_file(self, value):
        self._outfile.write(value)

    def close_and_write(self):
        self._outfile.close()

    def print_output_file(self):
        output_file_contents = open(
            self._outfile_path, mode='rt', encoding='utf-8')
        for line in output_file_contents:
            sys.stdout.write(line)

    def infile_name(self):
        return os.path.basename(self.infile_path)
