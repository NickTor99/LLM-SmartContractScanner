import unittest
from unittest.mock import patch
from cli.comands import RunCommand

class TestRunCommand(unittest.TestCase):
    @patch("cli.comands.run_pipeline")
    @patch("cli.comands.AppContext")
    def test_execute_success(self, mock_context, mock_pipeline):
        """
        Verifica che RunCommand invochi correttamente AppContext e run_pipeline.
        """
        cmd = RunCommand("gpt-4", "valid.teal", 2, 3)
        cmd.execute()
        mock_context.assert_called_once_with(model="gpt-4", vuln_limit=2, contract_limit=3)
        mock_pipeline.assert_called_once()

    @patch("cli.comands.run_pipeline")
    @patch("cli.comands.AppContext")
    def test_execute_model_missing(self, mock_context, mock_pipeline):
        """
        Verifica che RunCommand sollevi un errore se il modello non è disponibile nella config.
        """
        mock_context.side_effect = ValueError("Model not found")
        cmd = RunCommand("missing-model", "valid.teal", 2, 3)
        with self.assertRaises(ValueError):
            cmd.execute()
