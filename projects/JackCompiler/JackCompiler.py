import sys
import os
from CompilationEngine import CompilationEngine


class JackAnalyzer:
    _comp_eng = None

    def __init__(self, input_loc):
        self._input_loc = input_loc

        if os.path.isdir(input_loc):
            self._path = input_loc
            self._fileList = os.listdir(input_loc)

    def parse_directory(self):
        print("parsing directory:")
        # for each .jack file in the directory parse the file
        for fileName in self._fileList:
            if fileName.endswith(".jack"):
                self._input_loc = self._path + "/" + fileName
                print("parsing file:", self._input_loc)
                self.parse_file()

    def parse_file(self):
        # create a CompilationEngine from the xxx.jack input file
        outfile_path = self._input_loc.replace(".jack", ".vm")
        # print(outfile_path)
        self._comp_eng = CompilationEngine(input_stream=self._input_loc, output_stream=outfile_path)
        self._comp_eng.compile_class()
        self._comp_eng.close_outfile()


if __name__ == '__main__':
    infile_path = os.path.realpath(sys.argv[1])
    jack_analyzer = JackAnalyzer(infile_path)

    if os.path.isdir(infile_path):
        jack_analyzer.parse_directory()
    else:
        jack_analyzer.parse_file()

