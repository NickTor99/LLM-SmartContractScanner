import unittest
import os
from io import StringIO
from unittest.mock import patch
from src.main import main  # Assicurati che main accetti un filepath come argomento


def get_abs_path(file):
    curr_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(curr_dir, "test_contracts", file)


class TestSystemMain(unittest.TestCase):

    @patch("sys.stdout", new_callable=StringIO)
    def test_valid_contract(self, mock_stdout):
        main(get_abs_path("valid.teal"))
        output = mock_stdout.getvalue()
        self.assertIn("Analisi completata", output)  # o un'altra frase che conferma il successo

    @patch("sys.stdout", new_callable=StringIO)
    def test_empty_contract(self, mock_stdout):
        main(get_abs_path("empty.teal"))
        output = mock_stdout.getvalue()
        self.assertIn("Codice vuoto", output)  # sostituisci con il messaggio effettivo

    @patch("sys.stdout", new_callable=StringIO)
    def test_invalid_contract(self, mock_stdout):
        main(get_abs_path("invalid.teal"))
        output = mock_stdout.getvalue()
        self.assertIn("Errore durante l'analisi", output)  # sostituisci con il messaggio atteso

    @patch("sys.stdout", new_callable=StringIO)
    def test_file_not_found(self, mock_stdout):
        with self.assertRaises(FileNotFoundError):
            main(get_abs_path("notfound.teal"))


    @patch("sys.stdout", new_callable=StringIO)
    def test_directory_instead_of_file(self, mock_stdout):
        with self.assertRaises(FileNotFoundError):
            main(get_abs_path(""))



if __name__ == '__main__':
    unittest.main()
