import unittest

from eilib.database.codegen import main as codegen_main


# TODO: Normal tests
class TestCodeGen(unittest.TestCase):

    def test_codegen(self):
        codegen_main()


if __name__ == '__main__':
    unittest.main(module="test_codegen")
