import json
import os
import unittest
from unittest.mock import patch, MagicMock

from requests import Response

from cli.comands import RunCommand

class TestRunCommand(unittest.TestCase):

    def setUp(self):
        self.response = Response()
        data = {
            "status": "success",
            "results": [
                {
                    "vulnerability": "Arbitrary Delete",
                    "analysis": ""
                }
            ]
        }

        self.response._content = json.dumps(data).encode('utf-8')
        self.valid_path = os.path.join(os.path.dirname(__file__), "../integration_test/test_contracts/valid.teal")

    @patch("cli.comands.requests.post")
    @patch("cli.comands.HTMLReportGenerator.generate")
    def test_execute_success(self, mock_report, mock_post):
        """
        Verifica che RunCommand invochi correttamente AppContext e run_pipeline.
        """

        mock_post.return_value = self.response


        cmd = RunCommand("deepseek-chat", self.valid_path, 2, 3, out="report")
        cmd.execute()
        mock_report.assert_called_once()

    @patch("cli.comands.requests.post")
    @patch("cli.comands.HTMLReportGenerator.generate")
    def test_execute_model_missing(self, mock_context, mock_pipeline):
        """
        Verifica che RunCommand sollevi un errore se il modello non è disponibile nella config.
        """
        mock_context.side_effect = ValueError("Model not found")
        cmd = RunCommand("missing-model", self.valid_path, 2, 3, out=None)
        with self.assertRaises(ValueError):
            cmd.execute()

    @patch("cli.comands.requests.post")
    @patch("cli.comands.HTMLReportGenerator.generate")
    def test_execute_filepath_missing(self, mock_context, mock_pipeline):
        """
        Verifica che RunCommand sollevi un errore se il file non è presente nel sistema.
        """
        mock_pipeline.side_effect = FileNotFoundError("File not found")
        cmd = RunCommand("deepseek-chat", "", 2, 3, out=None)
        with self.assertRaises(FileNotFoundError):
            cmd.execute()


    @patch("cli.comands.requests.post")
    @patch("cli.comands.HTMLReportGenerator.generate")
    def test_execute_negative_limit(self, mock_context, mock_pipeline):
        """
        Verifica che RunCommand sollevi un errore se il modello non è disponibile nella config.
        """

        with self.assertRaises(ValueError):
            cmd = RunCommand("deepseek-chat", self.valid_path, -2, 3, out=None)
            cmd.execute()

        with self.assertRaises(ValueError):
            cmd = RunCommand("deepseek-chat", "valid.teal", 2, -3, out=None)
            cmd.execute()

    @patch("cli.comands.requests.post")
    @patch("cli.comands.HTMLReportGenerator.generate")
    def test_execute_zero_limit(self, mock_context, mock_pipeline):
        """
        Verifica che RunCommand sollevi un errore se il modello non è disponibile nella config.
        """

        with self.assertRaises(ValueError):
            cmd = RunCommand("deepseek-chat", self.valid_path, 0, 0, out=None)
            cmd.execute()

    # Change Request 2: Report output

    @patch("cli.comands.requests.post")
    @patch("cli.comands.HTMLReportGenerator.generate")
    def test_execute_with_out_path(self, mock_report, mock_post):

        mock_post.return_value = self.response


        cmd = RunCommand("deepseek-chat", self.valid_path, 2, 3, out=None)
        cmd.execute()
        mock_report.assert_called_once()

