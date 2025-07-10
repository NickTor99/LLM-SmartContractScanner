import io
import logging
import sys
import unittest
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))
print(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))
from io import StringIO
from unittest.mock import patch
from main import main


def get_abs_path(file):
    curr_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(curr_dir, "test_contracts", file)


class TestSystemMain(unittest.TestCase):

    @patch("sys.stdout", new_callable=StringIO)
    def test_valid_contract(self, mock_stdout):
        main(["run", "--filepath", get_abs_path("valid.teal"), "--model", "deepseek-chat"])
        output = mock_stdout.getvalue()
        self.assertIn("Analisi completata", output)

    def test_empty_contract(self):
        log_stream = io.StringIO()
        handler = logging.StreamHandler(log_stream)
        logger = logging.getLogger()
        logger.addHandler(handler)

        main(["run", "--filepath", get_abs_path("empty.teal"), "--model", "deepseek-chat"])

        handler.flush()
        logs = log_stream.getvalue()
        logger.removeHandler(handler)

        self.assertIn("Codice è vuoto", logs)

    @patch("sys.stdout", new_callable=StringIO)
    def test_invalid_contract(self, mock_stdout):

        log_stream = io.StringIO()
        handler = logging.StreamHandler(log_stream)
        logger = logging.getLogger()
        logger.addHandler(handler)

        main(["run", "--filepath", get_abs_path("invalid.teal"), "--model", "deepseek-chat"])

        handler.flush()
        logs = log_stream.getvalue()
        logger.removeHandler(handler)
        self.assertIn("Errore di sintassi", logs)

    def test_file_not_found(self):
        log_stream = io.StringIO()
        handler = logging.StreamHandler(log_stream)
        logger = logging.getLogger()
        logger.addHandler(handler)

        main(["run", "--filepath", get_abs_path("notfound.teal"), "--model", "deepseek-chat"])

        handler.flush()
        logs = log_stream.getvalue()
        logger.removeHandler(handler)
        self.assertIn("Error: Percorso", logs)

    @patch("sys.stdout", new_callable=StringIO)
    def test_directory_instead_of_file(self, mock_stdout):
        log_stream = io.StringIO()
        handler = logging.StreamHandler(log_stream)
        logger = logging.getLogger()
        logger.addHandler(handler)

        main(["run", "--filepath", get_abs_path(""), "--model", "deepseek-chat"])

        handler.flush()
        logs = log_stream.getvalue()
        logger.removeHandler(handler)
        self.assertIn("Error: Percorso", logs)

    @patch("sys.stdout", new_callable=StringIO)
    def test_model_list(self, mock_stdout):
        main(["model-list"])
        output = mock_stdout.getvalue()
        self.assertIn("Model name", output)

    @patch("sys.stdout", new_callable=StringIO)
    def test_set_model_hf(self, mock_stdout):
        main(["set-model", "--source", "huggingface", "--model_name", "sshleifer/tiny-gpt2"])
        output = mock_stdout.getvalue()
        self.assertIn("Modello impostato", output)

    @patch("sys.stdout", new_callable=StringIO)
    def test_set_model_openai(self, mock_stdout):
        main(["set-model", "--source", "openai", "--model_name", "sshleifer/tiny-gpt2", "--api_key", "sk-dcdscds2cds2v2ds2", "--base_url", "https://api.openai.com"])
        output = mock_stdout.getvalue()
        self.assertIn("Modello impostato", output)

    def test_set_model_openai_missing_apikey(self):
        log_stream = io.StringIO()
        handler = logging.StreamHandler(log_stream)
        logger = logging.getLogger()
        logger.addHandler(handler)

        main(["set-model", "--source", "openai", "--model_name", "gpt-4", "--base_url", "https://api.openai.com"])

        handler.flush()
        logs = log_stream.getvalue()
        logger.removeHandler(handler)

        self.assertIn("Error", logs)

    def test_run_missing_model(self):
        with self.assertRaises(SystemExit):
            main(["run", "--filepath", get_abs_path("valid.teal")])

    def test_command_not_found(self):
        with self.assertRaises(SystemExit):
            main(["not-found"])


if __name__ == '__main__':
    unittest.main()
