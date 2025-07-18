import unittest
from unittest.mock import patch, MagicMock
from cli.invoker import CLIInvoker
from cli.comands import RunCommand


class TestIntegrationCLIInvokerRunCommand(unittest.TestCase):

    @patch("cli.comands.run_pipeline")
    @patch("cli.comands.AppContext")
    def test_run_valid_model_and_file(self, mock_appcontext, mock_pipeline):
        """
        Test T1: File valido, modello installato
        Verifica che l'esecuzione del comando 'run' inizializzi AppContext
        e lanci correttamente la pipeline.
        """
        args = [
            "run",
            "--filepath", "contract.teal",
            "--model", "gpt-4",
            "--vuln-limit", "1",
            "--contract-limit", "2"
        ]
        cli = CLIInvoker()
        cli.set_command(args)
        cli.run_command()

        mock_appcontext.assert_called_once_with(model="gpt-4", vuln_limit=1, contract_limit=2)
        mock_pipeline.assert_called_once()

    @patch("cli.comands.run_pipeline")
    @patch("cli.comands.AppContext")
    def test_run_model_not_installed(self, mock_appcontext, mock_pipeline):
        """
        Test T2: File valido, modello non installato
        Simula un errore durante la costruzione del contesto.
        """
        mock_appcontext.side_effect = ValueError("Model not found")

        args = [
            "run",
            "--filepath", "contract.teal",
            "--model", "non-existent-model",
            "--vuln-limit", "1",
            "--contract-limit", "2"
        ]
        cli = CLIInvoker()
        cli.set_command(args)

        with self.assertRaises(ValueError):
            cli.run_command()

    @patch("cli.comands.run_pipeline")
    @patch("cli.comands.AppContext")
    def test_run_file_not_found(self, mock_appcontext, mock_pipeline):
        """
        Test T3-T4: File inesistente, modello qualsiasi
        Simula l'errore di file non trovato durante l'esecuzione della pipeline.
        """
        mock_pipeline.side_effect = FileNotFoundError("File not found")
        mock_appcontext.return_value = MagicMock()

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

    @patch("cli.comands.run_pipeline")
    @patch("cli.comands.AppContext")
    def test_run_file_model_not_installed(self, mock_appcontext, mock_pipeline):
        """
        Test T3-T4: File inesistente, modello non istallato
        Simula l'errore di file non trovato durante l'esecuzione della pipeline.
        """
        mock_pipeline.side_effect = FileNotFoundError("File not found")


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


    @patch("cli.comands.run_pipeline")
    @patch("cli.comands.AppContext")
    def test_run_with_out_param(self, mock_app_context, mock_pipeline):
        """
        T5: Esecuzione con parametro --out esplicitamente definito.
        """

        mock_generator = MagicMock()
        mock_context_instance = MagicMock()
        mock_context_instance.get_report_generator.return_value = mock_generator

        mock_app_context.return_value = mock_context_instance

        args = [
            "run",
            "--filepath", "contracts/test.teal",
            "--model", "gpt-4",
            "--vuln-limit", "2",
            "--contract-limit", "2",
            "--out", "output/custom-report.html"
        ]

        mock_pipeline.return_value = [{"vulnerability": "Arbitrary delete", "analysis": ""}]

        cli = CLIInvoker()
        cli.set_command(args)
        cli.run_command()

        mock_generator.generate.assert_called_once_with(
            results=mock_pipeline.return_value,
            file_path="contracts/test.teal",
            report_name="output/custom-report.html"
        )

    @patch("cli.comands.run_pipeline")
    @patch("cli.comands.AppContext")
    def test_run_without_out_param(self, mock_app_context, mock_pipeline):
        """
        T6: Esecuzione senza parametro --out.
        """
        mock_generator = MagicMock()
        mock_context_instance = MagicMock()
        mock_context_instance.get_report_generator.return_value = mock_generator

        mock_app_context.return_value = mock_context_instance

        args = [
            "run",
            "--filepath", "contracts/test.teal",
            "--model", "gpt-4",
            "--vuln-limit", "2",
            "--contract-limit", "2",
        ]

        mock_pipeline.return_value = [{"vulnerability": "Arbitrary delete", "analysis": ""}]

        cli = CLIInvoker()
        cli.set_command(args)
        cli.run_command()

        mock_generator.generate.assert_called_once_with(
            results=mock_pipeline.return_value,
            file_path="contracts/test.teal",
            report_name=None
        )

if __name__ == "__main__":
    unittest.main()
