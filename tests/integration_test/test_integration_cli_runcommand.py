import json
import os
import unittest
from io import StringIO
from unittest.mock import patch, MagicMock, mock_open

from requests import Response

from cli.invoker import CLIInvoker


class TestIntegrationCLIInvokerRunCommand(unittest.TestCase):

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

        self.response_fail = Response()
        data = {
            "status": "fail",
            "results": "errore"
        }

        self.response_fail._content = json.dumps(data).encode('utf-8')

        self.valid_path = os.path.join(os.path.dirname(__file__), "test_contracts/valid.teal")


    @patch("cli.comands.requests.post")
    @patch("cli.comands.HTMLReportGenerator")
    def test_run_valid_model_and_file(self, mock_report, mock_config):
        """
        Test T1: File valido, modello installato
        Verifica che l'esecuzione del comando 'run' inizializzi AppContext
        e lanci correttamente la pipeline.
        """

        mock_config.return_value = self.response

        args = [
            "run",
            "--filepath", self.valid_path,
            "--model", "gpt-4",
            "--vuln-limit", "1",
            "--contract-limit", "2"
        ]
        cli = CLIInvoker()
        cli.set_command(args)
        cli.run_command()

        mock_report.assert_called_once()



    @patch("cli.comands.requests.post")
    @patch("cli.comands.HTMLReportGenerator")
    def test_run_model_not_installed(self, mock_report, mock_config):
        """
        Test T2: File valido, modello non installato
        Simula un errore durante la costruzione del contesto.
        """
        mock_config.return_value = self.response_fail

        args = [
            "run",
            "--filepath", self.valid_path,
            "--model", "non-existent-model",
            "--vuln-limit", "1",
            "--contract-limit", "2"
        ]
        cli = CLIInvoker()
        cli.set_command(args)
        cli.run_command()

        mock_report.assert_not_called()

    @patch("cli.comands.requests.post")
    @patch("cli.comands.HTMLReportGenerator")
    def test_run_file_not_found(self, mock_report, mock_config):
        """
        Test T3-T4: File inesistente, modello qualsiasi
        """

        args = [
            "run",
            "--filepath", "nonexistent.teal",
            "--model", "gpt-4",
            "--vuln-limit", "1",
            "--contract-limit", "2"
        ]
        cli = CLIInvoker()
        cli.set_command(args)

        with self.assertRaises(FileNotFoundError):
            cli.run_command()


    def test_run_file_model_not_installed(self):
        """
        Test T3-T4: File inesistente, modello non istallato
        Simula l'errore di file non trovato durante l'esecuzione della pipeline.
        """

        args = [
            "run",
            "--filepath", "nonexistent.teal",
            "--model", "gpt-4",
            "--vuln-limit", "1",
            "--contract-limit", "2"
        ]
        cli = CLIInvoker()
        cli.set_command(args)

        with self.assertRaises(FileNotFoundError):
            cli.run_command()


    #Change Reiquest 2


    @patch("cli.comands.requests.post")
    @patch("cli.comands.HTMLReportGenerator.generate")
    def test_run_with_out_param(self, mock_report, mock_config):
        """
        T5: Esecuzione con parametro --out esplicitamente definito.
        """

        mock_config.return_value = self.response

        args = [
            "run",
            "--filepath", self.valid_path,
            "--model", "gpt-4",
            "--vuln-limit", "1",
            "--contract-limit", "2",
            "--out", "test"
        ]
        cli = CLIInvoker()
        cli.set_command(args)
        cli.run_command()

        mock_report.assert_called_once_with(
            results=self.response.json()["results"],
            file_path=self.valid_path,
            report_name="test",
        )

    @patch("cli.comands.requests.post")
    @patch("cli.comands.HTMLReportGenerator.generate")
    def test_run_without_out_param(self, mock_report, mock_config):
        """
        T6: Esecuzione senza parametro --out.
        """
        mock_config.return_value = self.response

        args = [
            "run",
            "--filepath", self.valid_path,
            "--model", "gpt-4",
            "--vuln-limit", "1",
            "--contract-limit", "2",
        ]
        cli = CLIInvoker()
        cli.set_command(args)
        cli.run_command()

        mock_report.assert_called_once_with(
            results=self.response.json()["results"],
            file_path=self.valid_path,
            report_name=None,
        )

if __name__ == "__main__":
    unittest.main()
