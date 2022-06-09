import sys
import os
from CompilationEngine import CompilationEngine


class JackAnalyzer:
    _comp_eng = None

    def __init__(self, input_loc):
        self._input_loc = input_loc

        if os.path.isdir(infile_path):
            self._fileList = os.listdir(infile_path)

    def parse_directory(self):
        # for each .jack file in the directory parse the file
        for fileName in self._fileList:
            if fileName.endswith(".jack"):
                self._input_loc = fileName
                self.parse_file()
                self.write_file_output()

    def parse_file(self):
        # create a CompilationEngine from the xxx.jack input file
        outfile_path = self._input_loc.replace(".jack", ".xml")
        self._comp_eng = CompilationEngine(input_stream=self._input_loc, output_stream=outfile_path)
        self._comp_eng.compile_class()

    def write_file_output(self):
        pass

    def create_output_file(self):
        # create an output file called xxx.xml
        pass


if __name__ == '__main__':
    infile_path = sys.argv[1]
    jack_analyzer = JackAnalyzer(infile_path)

    if os.path.isdir(infile_path):
        jack_analyzer.parse_directory()
    else:
        jack_analyzer.parse_file()

