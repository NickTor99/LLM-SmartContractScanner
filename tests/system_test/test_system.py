import sys
import unittest
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))
print(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))
from io import StringIO
from unittest.mock import patch
from cli_shell import cli_shell




def get_abs_path(file):
    curr_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(curr_dir, "test_contracts", file)


class TestSystemMain(unittest.TestCase):

    @patch("sys.stdout", new_callable=StringIO)
    def test_valid_contract(self, mock_stdout):
        cli_shell(get_abs_path("valid.teal"))
        output = mock_stdout.getvalue()
        self.assertIn("Analisi completata", output)

    @patch("sys.stdout", new_callable=StringIO)
    def test_empty_contract(self, mock_stdout):
        cli_shell(get_abs_path("empty.teal"))
        output = mock_stdout.getvalue()
        self.assertIn("Codice è vuoto", output)

    @patch("sys.stdout", new_callable=StringIO)
    def test_invalid_contract(self, mock_stdout):
        cli_shell(get_abs_path("invalid.teal"))
        output = mock_stdout.getvalue()
        self.assertIn("Errore di sintassi", output)

    @patch("sys.stdout", new_callable=StringIO)
    def test_file_not_found(self, mock_stdout):
        with self.assertRaises(FileNotFoundError):
            cli_shell(get_abs_path("notfound.teal"))


    @patch("sys.stdout", new_callable=StringIO)
    def test_directory_instead_of_file(self, mock_stdout):
        with self.assertRaises(FileNotFoundError):
            cli_shell(get_abs_path(""))



if __name__ == '__main__':
    unittest.main()
