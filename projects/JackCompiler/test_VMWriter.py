import unittest
from VMWriter import VMWriter
from io import StringIO


class VMWriterTest(unittest.TestCase):
    def setUp(self):
        self._mock_in_file = StringIO()

    def tearDown(self):
        self._mock_in_file.close()

    def test_write_push(self):
        vm_writer = VMWriter(self._mock_in_file)
        vm_writer.write_push("constant", 1)
        vm_writer._outfile.seek(0)
        line = vm_writer._outfile.readline()
        self.assertEqual("push constant 1\n", line)

    def test_write_pop(self):
        vm_writer = VMWriter(self._mock_in_file)
        vm_writer.write_pop("local", 1)
        vm_writer._outfile.seek(0)
        line = vm_writer._outfile.readline()
        self.assertEqual("pop local 1\n", line)

    def test_write_arithmetic(self):
        vm_writer = VMWriter(self._mock_in_file)
        vm_writer.write_arithmetic("gt")
        vm_writer._outfile.seek(0)
        line = vm_writer._outfile.readline()
        self.assertEqual("gt\n", line)

    def test_write_label(self):
        vm_writer = VMWriter(self._mock_in_file)
        vm_writer.write_label("loop")
        vm_writer._outfile.seek(0)
        line = vm_writer._outfile.readline()
        self.assertEqual("label loop\n", line)

    def test_write_goto(self):
        vm_writer = VMWriter(self._mock_in_file)
        vm_writer.write_goto("end")
        vm_writer._outfile.seek(0)
        line = vm_writer._outfile.readline()
        self.assertEqual("goto end\n", line)

    def test_write_if(self):
        vm_writer = VMWriter(self._mock_in_file)
        vm_writer.write_if("loop")
        vm_writer._outfile.seek(0)
        line = vm_writer._outfile.readline()
        self.assertEqual("if-goto loop\n", line)

    def test_write_call(self):
        vm_writer = VMWriter(self._mock_in_file)
        vm_writer.write_call("distance", 2)
        vm_writer._outfile.seek(0)
        line = vm_writer._outfile.readline()
        self.assertEqual("call distance 2\n", line)

    def test_write_function(self):
        vm_writer = VMWriter(self._mock_in_file)
        vm_writer.write_function("distance", 1)
        vm_writer._outfile.seek(0)
        line = vm_writer._outfile.readline()
        self.assertEqual("function distance 1\n", line)

    def test_write_return(self):
        vm_writer = VMWriter(self._mock_in_file)
        vm_writer.write_return()
        vm_writer._outfile.seek(0)
        line = vm_writer._outfile.readline()
        self.assertEqual("return\n", line)
