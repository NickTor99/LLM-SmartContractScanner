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
        cmd = RunCommand("deepseek-chat", "valid.teal", 2, 3)
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

    @patch("cli.comands.run_pipeline")
    @patch("cli.comands.AppContext")
    def test_execute_filepath_missing(self, mock_context, mock_pipeline):
        """
        Verifica che RunCommand sollevi un errore se il modello non è disponibile nella config.
        """
        mock_pipeline.side_effect = FileNotFoundError("File not found")
        cmd = RunCommand("deepseek-chat", "", 2, 3)
        with self.assertRaises(ValueError):
            cmd.execute()


    @patch("cli.comands.run_pipeline")
    @patch("cli.comands.AppContext")
    def test_execute_negative_limit(self, mock_context, mock_pipeline):
        """
        Verifica che RunCommand sollevi un errore se il modello non è disponibile nella config.
        """
        cmd = RunCommand("deepseek-chat", "valid.teal", -2, 3)
        with self.assertRaises(ValueError):
            cmd.execute()

        cmd = RunCommand("deepseek-chat", "valid.teal", 2, -3)
        with self.assertRaises(ValueError):
            cmd.execute()

    @patch("cli.comands.run_pipeline")
    @patch("cli.comands.AppContext")
    def test_execute_zero_limit(self, mock_context, mock_pipeline):
        """
        Verifica che RunCommand sollevi un errore se il modello non è disponibile nella config.
        """

        cmd = RunCommand("deepseek-chat", "valid.teal", 0, 0)
        with self.assertRaises(ValueError):
            cmd.execute()

    # Change Request 2: Report output

    @patch("cli.comands.run_pipeline")
    @patch("cli.comands.AppContext")
    def test_execute_with_out_path(self, mock_context, mock_pipeline):
        """
        RC7: out specificato => il report deve essere generato nella directory fornita.
        """
        cmd = RunCommand("gpt-4", "valid.teal", 2, 3, out="output/report.html")
        cmd.execute()
        mock_context.assert_called_once_with(model="gpt-4", vuln_limit=2, contract_limit=3, out_path="output/report.html")
        mock_pipeline.assert_called_once()


    @patch("cli.comands.run_pipeline")
    @patch("cli.comands.AppContext")
    def test_execute_without_out_path(self, mock_context, mock_pipeline):
        """
        RC8: out non specificato => il report deve essere generato nel percorso predefinito.
        """
        cmd = RunCommand("gpt-4", "valid.teal", 2, 3, out=None)
        cmd.execute()
        mock_context.assert_called_once_with(model="gpt-4", vuln_limit=2, contract_limit=3, out_path=None)
        mock_pipeline.assert_called_once()
